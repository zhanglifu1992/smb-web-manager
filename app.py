import json
import logging
import os
import platform
import subprocess
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file

app = Flask(__name__)
app.config['CONFIG_FILE'] = 'config.json'
app.config['LOG_FILE'] = 'smb_web_manager.log'

# 设置日志
logging.basicConfig(
    filename=app.config['LOG_FILE'],
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def load_config():
    """加载配置文件"""
    config_file = app.config['CONFIG_FILE']
    
    # 如果配置文件不存在，创建默认配置
    if not os.path.exists(config_file):
        default_config = {
            "mounts": [],
            "system": {
                "platform": platform.system(),
                "last_update": datetime.now().isoformat()
            }
        }
        save_config(default_config)
        return default_config
    
    # 如果配置文件存在但为空或无效
    try:
        with open(config_file, 'r') as f:
            # 检查文件是否为空
            content = f.read().strip()
            if not content:
                raise ValueError("配置文件为空")
            
            return json.loads(content)
    except (json.JSONDecodeError, ValueError) as e:
        logging.error(f"配置文件解析错误: {e}，将使用默认配置")
        
        # 备份损坏的配置文件
        if os.path.exists(config_file):
            backup_file = f"{config_file}.bak.{datetime.now().strftime('%Y%m%d%H%M%S')}"
            os.rename(config_file, backup_file)
            logging.info(f"已备份损坏的配置文件到: {backup_file}")
        
        # 创建默认配置
        default_config = {
            "mounts": [],
            "system": {
                "platform": platform.system(),
                "last_update": datetime.now().isoformat()
            }
        }
        save_config(default_config)
        return default_config

def save_config(config):
    """保存配置文件"""
    config['system']['last_update'] = datetime.now().isoformat()
    with open(app.config['CONFIG_FILE'], 'w') as f:
        json.dump(config, f, indent=2)

def log_action(action, details):
    """记录操作日志"""
    logging.info(f"{action}: {details}")
    return True

def get_system_info():
    """获取系统信息"""
    system = platform.system()
    info = {
        "system": system,
        "hostname": platform.node(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine()
    }
    return info

def execute_command(cmd):
    """执行系统命令"""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=30
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "stdout": "",
            "stderr": "Command timed out",
            "returncode": -1
        }
    except Exception as e:
        return {
            "success": False,
            "stdout": "",
            "stderr": str(e),
            "returncode": -1
        }

# 上下文处理器 - 确保所有模板都能访问 system_info
@app.context_processor
def inject_system_info():
    return {'system_info': get_system_info()}

@app.route('/')
def index():
    """主页面"""
    config = load_config()
    return render_template('index.html', mounts=config['mounts'])

@app.route('/config')
def config_page():
    """配置管理页面"""
    config = load_config()
    return render_template('config.html', mounts=config['mounts'])

@app.route('/logs')
def logs_page():
    """日志查看页面"""
    return render_template('logs.html')

@app.route('/api/mounts', methods=['GET'])
def get_mounts():
    """获取所有挂载配置"""
    config = load_config()
    return jsonify(config['mounts'])

@app.route('/api/mounts', methods=['POST'])
def add_mount():
    """添加挂载配置"""
    config = load_config()
    new_mount = request.json
    
    # 验证必要字段
    required_fields = ['name', 'server', 'share', 'mount_point', 'username']
    for field in required_fields:
        if field not in new_mount:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    # 设置ID
    if not config['mounts']:
        new_mount['id'] = 1
    else:
        new_mount['id'] = max(m['id'] for m in config['mounts']) + 1
    
    # 设置默认值
    new_mount.setdefault('password', '')
    new_mount.setdefault('options', '')
    new_mount.setdefault('auto_mount', False)
    new_mount.setdefault('is_mounted', False)
    
    config['mounts'].append(new_mount)
    save_config(config)
    log_action("ADD_MOUNT", f"Added mount: {new_mount['name']}")
    
    return jsonify(new_mount), 201

@app.route('/api/mounts/<int:mount_id>', methods=['PUT'])
def update_mount(mount_id):
    """更新挂载配置"""
    config = load_config()
    updated_data = request.json
    
    for i, mount in enumerate(config['mounts']):
        if mount['id'] == mount_id:
            # 保留一些字段不变
            preserved_fields = ['id', 'is_mounted']
            for field in preserved_fields:
                if field in mount:
                    updated_data[field] = mount[field]
            
            config['mounts'][i] = updated_data
            save_config(config)
            log_action("UPDATE_MOUNT", f"Updated mount: {updated_data['name']}")
            return jsonify(updated_data)
    
    return jsonify({"error": "Mount not found"}), 404

@app.route('/api/mounts/<int:mount_id>', methods=['DELETE'])
def delete_mount(mount_id):
    """删除挂载配置"""
    config = load_config()
    
    for i, mount in enumerate(config['mounts']):
        if mount['id'] == mount_id:
            # 如果已挂载，先卸载
            if mount.get('is_mounted', False):
                unmount_result = perform_unmount(mount)
                if not unmount_result['success']:
                    return jsonify({"error": "Cannot delete mounted share. Unmount first."}), 400
            
            deleted_mount = config['mounts'].pop(i)
            save_config(config)
            log_action("DELETE_MOUNT", f"Deleted mount: {deleted_mount['name']}")
            return jsonify({"message": "Mount deleted"})
    
    return jsonify({"error": "Mount not found"}), 404

@app.route('/api/mounts/<int:mount_id>/mount', methods=['POST'])
def mount_share_api(mount_id):
    """挂载SMB共享"""
    config = load_config()
    
    for i, mount in enumerate(config['mounts']):
        if mount['id'] == mount_id:
            if mount.get('is_mounted', False):
                return jsonify({"error": "Share is already mounted"}), 400
            
            result = perform_mount(mount)
            if result['success']:
                config['mounts'][i]['is_mounted'] = True
                save_config(config)
                log_action("MOUNT_SUCCESS", f"Mounted: {mount['name']}")
                return jsonify({"message": "Mount successful", "details": result})
            else:
                log_action("MOUNT_FAILED", f"Failed to mount: {mount['name']} - {result['stderr']}")
                return jsonify({"error": "Mount failed", "details": result}), 500
    
    return jsonify({"error": "Mount not found"}), 404

@app.route('/api/mounts/<int:mount_id>/unmount', methods=['POST'])
def unmount_share_api(mount_id):
    """卸载SMB共享"""
    config = load_config()
    
    for i, mount in enumerate(config['mounts']):
        if mount['id'] == mount_id:
            if not mount.get('is_mounted', False):
                return jsonify({"error": "Share is not mounted"}), 400
            
            result = perform_unmount(mount)
            if result['success']:
                config['mounts'][i]['is_mounted'] = False
                save_config(config)
                log_action("UNMOUNT_SUCCESS", f"Unmounted: {mount['name']}")
                return jsonify({"message": "Unmount successful", "details": result})
            else:
                log_action("UNMOUNT_FAILED", f"Failed to unmount: {mount['name']} - {result['stderr']}")
                return jsonify({"error": "Unmount failed", "details": result}), 500
    
    return jsonify({"error": "Mount not found"}), 404

@app.route('/api/system/info', methods=['GET'])
def system_info():
    """获取系统信息"""
    return jsonify(get_system_info())

@app.route('/api/logs', methods=['GET'])
def get_logs():
    """获取日志内容"""
    log_file = app.config['LOG_FILE']
    try:
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                logs = f.readlines()
            return jsonify({"logs": logs[-100:]})  # 返回最后100行日志
        else:
            return jsonify({"logs": ["日志文件不存在"]})
    except Exception as e:
        return jsonify({"logs": [f"读取日志失败: {str(e)}"]})

@app.route('/api/logs/clear', methods=['POST'])
def clear_logs():
    """清空日志"""
    try:
        with open(app.config['LOG_FILE'], 'w') as f:
            f.write('')
        log_action("CLEAR_LOGS", "Logs cleared")
        return jsonify({"message": "日志已清空"})
    except Exception as e:
        return jsonify({"error": f"清空日志失败: {str(e)}"}), 500

def perform_mount(mount_config):
    """执行挂载操作"""
    system = platform.system()
    
    if system == "Darwin":  # macOS
        # 创建挂载点目录
        os.makedirs(mount_config['mount_point'], exist_ok=True)
        
        # 构建mount_smbfs命令
        cmd = f"mount -t smbfs '//{mount_config['username']}:{mount_config['password']}@{mount_config['server']}/{mount_config['share']}' '{mount_config['mount_point']}'"
        
    elif system == "Linux":
        # 创建挂载点目录
        os.makedirs(mount_config['mount_point'], exist_ok=True)
        
        # 构建mount.cifs命令
        cmd = f"mount -t cifs '//{mount_config['server']}/{mount_config['share']}' '{mount_config['mount_point']}' -o username={mount_config['username']},password={mount_config['password']}"
        
    elif system == "Windows":
        # Windows使用net use命令
        drive_letter = mount_config.get('drive_letter', 'Z:')
        cmd = f"net use {drive_letter} '\\\\{mount_config['server']}\\{mount_config['share']}' {mount_config['password']} /user:{mount_config['username']}"
        
    else:
        return {
            "success": False,
            "stderr": f"Unsupported platform: {system}",
            "returncode": -1
        }
    
    return execute_command(cmd)

def perform_unmount(mount_config):
    """执行卸载操作"""
    system = platform.system()
    
    if system == "Darwin":  # macOS
        cmd = f"umount '{mount_config['mount_point']}'"
    elif system == "Linux":
        cmd = f"umount '{mount_config['mount_point']}'"
    elif system == "Windows":
        drive_letter = mount_config.get('drive_letter', 'Z:')
        cmd = f"net use {drive_letter} /delete"
    else:
        return {
            "success": False,
            "stderr": f"Unsupported platform: {system}",
            "returncode": -1
        }
    
    return execute_command(cmd)

if __name__ == '__main__':
    # 确保必要的目录存在
    if not os.path.exists('static'):
        os.makedirs('static')
    if not os.path.exists('static/css'):
        os.makedirs('static/css')
    if not os.path.exists('static/js'):
        os.makedirs('static/js')
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # 初始化配置文件
    load_config()
    
    app.run(host='0.0.0.0', port=5555, debug=True)

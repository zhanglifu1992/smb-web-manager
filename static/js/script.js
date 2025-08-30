// 挂载单个共享
function mountShare(mountId) {
    fetch(`/api/mounts/${mountId}/mount`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(`挂载失败: ${data.error}`);
        } else {
            alert('挂载成功');
            refreshStatus();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('操作失败，请查看日志');
    });
}

// 卸载单个共享
function unmountShare(mountId) {
    fetch(`/api/mounts/${mountId}/unmount`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(`卸载失败: ${data.error}`);
        } else {
            alert('卸载成功');
            refreshStatus();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('操作失败，请查看日志');
    });
}

// 挂载所有共享
function mountAll() {
    if (!confirm('确定要挂载所有共享吗？')) return;
    
    fetch('/api/mounts')
    .then(response => {
        if (!response.ok) {
            throw new Error('获取挂载列表失败');
        }
        return response.json();
    })
    .then(mounts => {
        const unmounted = mounts.filter(m => !m.is_mounted);
        let promises = [];
        
        unmounted.forEach(mount => {
            promises.push(
                fetch(`/api/mounts/${mount.id}/mount`, { method: 'POST' })
                .then(response => response.json())
            );
        });
        
        return Promise.all(promises);
    })
    .then(results => {
        const successes = results.filter(r => !r.error).length;
        alert(`操作完成，成功挂载 ${successes} 个共享`);
        refreshStatus();
    })
    .catch(error => {
        console.error('Error:', error);
        alert('操作失败，请查看日志');
    });
}

// 卸载所有共享
function unmountAll() {
    if (!confirm('确定要卸载所有共享吗？')) return;
    
    fetch('/api/mounts')
    .then(response => {
        if (!response.ok) {
            throw new Error('获取挂载列表失败');
        }
        return response.json();
    })
    .then(mounts => {
        const mounted = mounts.filter(m => m.is_mounted);
        let promises = [];
        
        mounted.forEach(mount => {
            promises.push(
                fetch(`/api/mounts/${mount.id}/unmount`, { method: 'POST' })
                .then(response => response.json())
            );
        });
        
        return Promise.all(promises);
    })
    .then(results => {
        const successes = results.filter(r => !r.error).length;
        alert(`操作完成，成功卸载 ${successes} 个共享`);
        refreshStatus();
    })
    .catch(error => {
        console.error('Error:', error);
        alert('操作失败，请查看日志');
    });
}

// 刷新状态
function refreshStatus() {
    window.location.reload();
}

// 删除配置
function deleteConfig(mountId) {
    if (!confirm('确定要删除此配置吗？此操作不可撤销。')) return;
    
    fetch(`/api/mounts/${mountId}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(`删除失败: ${data.error}`);
        } else {
            alert('删除成功');
            window.location.reload();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('操作失败，请查看日志');
    });
}

// 添加配置表单提交
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('add-mount-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());
            
            fetch('/api/mounts', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(`添加失败: ${data.error}`);
                } else {
                    alert('添加成功');
                    window.location.reload();
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('操作失败，请查看日志');
            });
        });
    }
    
    // 加载日志
    refreshLogs();
});

// 刷新日志
function refreshLogs() {
    fetch('/api/logs')
    .then(response => response.json())
    .then(data => {
        const logContent = document.getElementById('log-content');
        if (logContent) {
            logContent.textContent = data.logs.join('');
            logContent.scrollTop = logContent.scrollHeight;
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// 清除日志
function clearLogs() {
    if (!confirm('确定要清除所有日志吗？此操作不可撤销。')) return;
    
    fetch('/api/logs/clear', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(`清除日志失败: ${data.error}`);
        } else {
            alert('日志已清空');
            refreshLogs();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('操作失败');
    });
}


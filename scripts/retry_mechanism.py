#!/usr/bin/env python3
"""
自动重试机制
为关键任务提供自动重试功能
"""

import time
import functools
from datetime import datetime
from pathlib import Path

# 重试日志文件
RETRY_LOG = Path("/workspace/projects/workspace/memory/logs/retry-log.md")

def log_retry(task_name, attempt, max_attempts, error, status):
    """记录重试日志"""
    RETRY_LOG.parent.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {task_name} - 尝试 {attempt}/{max_attempts} - {status}"
    if error:
        log_entry += f" - 错误: {str(error)[:100]}"
    log_entry += "\n"
    
    with open(RETRY_LOG, "a") as f:
        f.write(log_entry)

def retry_with_backoff(max_attempts=3, initial_delay=1, backoff_factor=2, 
                       exceptions=(Exception,), on_failure=None):
    """
    自动重试装饰器
    
    Args:
        max_attempts: 最大重试次数（默认3次）
        initial_delay: 初始延迟（秒，默认1秒）
        backoff_factor: 退避因子（默认2，即1s, 2s, 4s）
        exceptions: 需要捕获的异常类型
        on_failure: 最终失败时的回调函数
    
    Returns:
        装饰器函数
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            task_name = func.__name__
            delay = initial_delay
            
            for attempt in range(1, max_attempts + 1):
                try:
                    result = func(*args, **kwargs)
                    if attempt > 1:
                        log_retry(task_name, attempt, max_attempts, None, "✅ 成功")
                    return result
                    
                except exceptions as e:
                    error_msg = str(e)
                    
                    if attempt < max_attempts:
                        log_retry(task_name, attempt, max_attempts, e, f"⏳ 失败，{delay}秒后重试")
                        time.sleep(delay)
                        delay *= backoff_factor
                    else:
                        log_retry(task_name, attempt, max_attempts, e, "❌ 最终失败")
                        
                        # 调用失败回调
                        if on_failure:
                            on_failure(task_name, e, args, kwargs)
                        
                        # 抛出最终异常
                        raise
            
            return None
        
        return wrapper
    return decorator

def retry_task(task_func, task_name="任务", max_attempts=3, 
               initial_delay=1, backoff_factor=2):
    """
    对单个任务执行重试
    
    Args:
        task_func: 要执行的任务函数（无参数lambda）
        task_name: 任务名称（用于日志）
        max_attempts: 最大重试次数
        initial_delay: 初始延迟
        backoff_factor: 退避因子
    
    Returns:
        (success: bool, result: any, error: Exception)
    """
    delay = initial_delay
    
    for attempt in range(1, max_attempts + 1):
        try:
            result = task_func()
            if attempt > 1:
                log_retry(task_name, attempt, max_attempts, None, "✅ 成功")
            return (True, result, None)
            
        except Exception as e:
            if attempt < max_attempts:
                log_retry(task_name, attempt, max_attempts, e, f"⏳ 失败，{delay}秒后重试")
                time.sleep(delay)
                delay *= backoff_factor
            else:
                log_retry(task_name, attempt, max_attempts, e, "❌ 最终失败")
                return (False, None, e)
    
    return (False, None, None)

class TaskWithRetry:
    """带重试机制的任务类"""
    
    def __init__(self, task_func, task_name, max_attempts=3, 
                 initial_delay=1, backoff_factor=2):
        self.task_func = task_func
        self.task_name = task_name
        self.max_attempts = max_attempts
        self.initial_delay = initial_delay
        self.backoff_factor = backoff_factor
        self.attempt_count = 0
        self.last_error = None
    
    def execute(self):
        """执行任务，带重试"""
        delay = self.initial_delay
        
        for attempt in range(1, self.max_attempts + 1):
            self.attempt_count = attempt
            
            try:
                result = self.task_func()
                
                if attempt > 1:
                    log_retry(self.task_name, attempt, self.max_attempts, None, "✅ 成功")
                
                return {
                    "success": True,
                    "result": result,
                    "attempts": attempt,
                    "error": None
                }
                
            except Exception as e:
                self.last_error = e
                
                if attempt < self.max_attempts:
                    log_retry(self.task_name, attempt, self.max_attempts, e, 
                             f"⏳ 失败，{delay}秒后重试")
                    time.sleep(delay)
                    delay *= self.backoff_factor
                else:
                    log_retry(self.task_name, attempt, self.max_attempts, e, "❌ 最终失败")
        
        return {
            "success": False,
            "result": None,
            "attempts": self.attempt_count,
            "error": self.last_error
        }

def get_retry_log():
    """获取重试日志内容"""
    if RETRY_LOG.exists():
        with open(RETRY_LOG) as f:
            return f.read()
    return "暂无重试记录"

# 常用任务的预配置重试
retry_3_times = retry_with_backoff(max_attempts=3, initial_delay=1)
retry_5_times = retry_with_backoff(max_attempts=5, initial_delay=1)

# 网络请求专用（更长延迟）
retry_network = retry_with_backoff(
    max_attempts=3, 
    initial_delay=2, 
    backoff_factor=2
)

# 文件操作专用
def retry_edit_file(file_path, edit_func, max_attempts=3):
    """
    带重试的文件编辑
    
    Args:
        file_path: 文件路径
        edit_func: 编辑函数，接收文件内容，返回修改后的内容
        max_attempts: 最大重试次数
    
    Returns:
        (success, result)
    """
    def task():
        with open(file_path, 'r') as f:
            content = f.read()
        
        new_content = edit_func(content)
        
        with open(file_path, 'w') as f:
            f.write(new_content)
        
        return True
    
    return retry_task(task, f"编辑文件 {file_path}", max_attempts)

if __name__ == "__main__":
    # 测试重试机制
    print("🔄 测试自动重试机制\n")
    
    # 测试1: 装饰器方式
    @retry_with_backoff(max_attempts=3, initial_delay=0.5)
    def test_task_success():
        """测试成功任务"""
        return "任务成功"
    
    @retry_with_backoff(max_attempts=3, initial_delay=0.5)
    def test_task_fail():
        """测试失败任务"""
        raise Exception("模拟错误")
    
    print("测试1: 成功任务")
    result = test_task_success()
    print(f"结果: {result}\n")
    
    print("测试2: 失败任务（会重试3次）")
    try:
        test_task_fail()
    except Exception as e:
        print(f"最终失败: {e}\n")
    
    # 测试3: 函数方式
    print("测试3: 使用retry_task函数")
    def my_task():
        return "任务完成"
    
    success, result, error = retry_task(my_task, "我的任务", max_attempts=2, initial_delay=0.5)
    print(f"成功: {success}, 结果: {result}, 错误: {error}\n")
    
    # 查看日志
    print("📋 重试日志:")
    print(get_retry_log())

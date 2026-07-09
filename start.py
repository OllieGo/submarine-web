import subprocess
import os
import sys
import signal

def main():
    project_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(project_dir, 'backend')
    frontend_dir = os.path.join(project_dir, 'frontend')

    print("[INFO] 正在启动潜望量化服务...")
    print("=" * 50)

    backend_proc = subprocess.Popen(
        [sys.executable, 'main.py'],
        cwd=backend_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding='utf-8',
        errors='replace'
    )

    frontend_proc = subprocess.Popen(
        ['cmd', '/c', 'npm', 'run', 'dev'],
        cwd=frontend_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding='utf-8',
        errors='replace'
    )

    print(f"[INFO] 后端服务 PID: {backend_proc.pid}")
    print(f"[INFO] 前端服务 PID: {frontend_proc.pid}")
    print("=" * 50)
    print("[INFO] 前端地址: http://localhost:5173")
    print("[INFO] 后端地址: http://localhost:3000")
    print("=" * 50)
    print("[INFO] 按 Ctrl+C 停止所有服务")
    print("")

    def print_output(proc, label):
        while True:
            try:
                line = proc.stdout.readline()
                if not line:
                    break
                print(f"[{label}] {line.rstrip()}")
            except Exception as e:
                print(f"[{label}] [ERROR] Read output failed: {e}")
                break

    import threading
    t1 = threading.Thread(target=print_output, args=(backend_proc, 'BACKEND'), daemon=True)
    t2 = threading.Thread(target=print_output, args=(frontend_proc, 'FRONTEND'), daemon=True)
    t1.start()
    t2.start()

    try:
        while True:
            if backend_proc.poll() is not None:
                print(f"[ERROR] 后端服务意外退出，退出码: {backend_proc.returncode}")
                break
            if frontend_proc.poll() is not None:
                print(f"[ERROR] 前端服务意外退出，退出码: {frontend_proc.returncode}")
                break
            import time
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[INFO] 正在停止服务...")
    finally:
        if backend_proc.poll() is None:
            backend_proc.terminate()
            backend_proc.wait()
            print("[INFO] 后端服务已停止")
        if frontend_proc.poll() is None:
            frontend_proc.terminate()
            frontend_proc.wait()
            print("[INFO] 前端服务已停止")
        print("=" * 50)
        print("[INFO] 所有服务已停止")

if __name__ == "__main__":
    main()
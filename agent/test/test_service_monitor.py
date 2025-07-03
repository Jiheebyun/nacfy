from jobs.service_monitor import monitor_services

if __name__ == "__main__":
    services = ['nginx', 'sshd', 'cron']
    results = monitor_services(services)
    for r in results:
        print(f"{r['service']}: {'ACTIVE' if r['is_active'] else 'INACTIVE'}")
        if r['error']:
            print(f"  Error: {r['error']}")
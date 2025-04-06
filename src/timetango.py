import datetime
import csv

class TimeTango:
    def __init__(self):
        self.projects = {}

    def log_time(self, project_name, start_time, end_time):
        if project_name not in self.projects:
            self.projects[project_name] = []
        self.projects[project_name].append((start_time, end_time))

    def calculate_billable_hours(self, project_name):
        if project_name not in self.projects:
            return 0.0
        
        total_hours = 0.0
        for start, end in self.projects[project_name]:
            duration = end - start
            total_hours += duration.total_seconds() / 3600.0
        
        return round(total_hours, 2)

    def generate_client_report(self, project_name, client_name):
        if project_name not in self.projects:
            return "No data available for this project."
        
        report = f"Client Report for {client_name}\n"
        report += f"Project: {project_name}\n\n"
        report += "Time Entries:\n"
        
        total_hours = 0.0
        for i, (start, end) in enumerate(self.projects[project_name], 1):
            duration = end - start
            hours = duration.total_seconds() / 3600.0
            report += f"Entry {i}: {start} - {end} ({round(hours, 2)} hours)\n"
            total_hours += hours
        
        report += f"\nTotal Billable Hours: {round(total_hours, 2)} hours"
        
        return report

    def save_to_csv(self, filename):
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Project', 'Start Time', 'End Time'])
            for project, entries in self.projects.items():
                for start, end in entries:
                    writer.writerow([project, start, end])

    def load_from_csv(self, filename):
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header
            for row in reader:
                project, start_str, end_str = row
                start = datetime.datetime.strptime(start_str, "%Y-%m-%d %H:%M:%S")
                end = datetime.datetime.strptime(end_str, "%Y-%m-%d %H:%M:%S")
                self.log_time(project, start, end)

# Example usage
if __name__ == "__main__":
    tango = TimeTango()

    # Log some time entries
    tango.log_time("Project A", datetime.datetime(2023, 5, 1, 9, 0), datetime.datetime(2023, 5, 1, 12, 0))
    tango.log_time("Project A", datetime.datetime(2023, 5, 2, 10, 0), datetime.datetime(2023, 5, 2, 13, 0))
    tango.log_time("Project B", datetime.datetime(2023, 5, 3, 14, 0), datetime.datetime(2023, 5, 3, 16, 0))

    # Calculate billable hours
    print(f"Billable hours for Project A: {tango.calculate_billable_hours('Project A')} hours")

    # Generate client report
    report = tango.generate_client_report("Project A", "Client X")
    print(report)

    # Save to CSV
    tango.save_to_csv("time_entries.csv")

    # Load from CSV
    new_tango = TimeTango()
    new_tango.load_from_csv("time_entries.csv")
    print(f"Billable hours for Project A after loading: {new_tango.calculate_billable_hours('Project A')} hours")
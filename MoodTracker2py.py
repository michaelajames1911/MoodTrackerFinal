import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from argparse import ArgumentParser


class MoodTracker:
    def __init__(self):
        self.df = pd.DataFrame(columns=['name', 'date', 'mood', 'context', 'severity'])

    def add_entry(self):
        """
        Add a new mood entry to the DataFrame.
        """
        print("Welcome to your personal Mood Tracker!")
        name = input("Enter your name: ")
        date = input("Enter the date (YYYY-MM-DD): ")
        mood = input("What mood are you feeling? (sad, happy, surprised, bad, fearful, angry, disgusted): ")

        valid_moods = ['sad', 'happy', 'surprised', 'bad', 'fearful', 'angry', 'disgusted']
        if mood not in valid_moods:
            print("Invalid mood entered. Please choose a valid mood.")
            return

        context = input("Why are you feeling this way? ")
        severity = input("On a scale of 1-10, how severe is this emotion? ")

        try:
            severity = int(severity)
        except ValueError:
            print("Invalid severity. Please enter a number between 1 and 10.")
            return
        
        if not (1 <= severity <= 10):
            print("Severity must be between 1 and 10.")
            return

        new_entry = pd.DataFrame({
            'name': [name],
            'date': [date],
            'mood': [mood],
            'context': [context],
            'severity': [severity]
        })
        try:
            self.df = pd.read_csv('mood_data.csv')
        except FileNotFoundError:
            self.df = pd.DataFrame(columns=['name', 'date', 'mood', 'context', 'severity'])

        self.df = pd.concat([self.df, new_entry], ignore_index=True)

        self.df.to_csv('mood_data.csv', index=False)
        print(f"Entry for {name} on {date} saved successfully!")

    def view_entries(self):
        """
        Display all past entries from the CSV.
        """
        try:
            self.df = pd.read_csv('mood_data.csv')
            print("\nYour previous entries:")
            print(self.df)
        except FileNotFoundError:
            print("No past entries found. Please add an entry first.")

    def plot_previous_entries(self):
        """
        Create a seaborn plot of the last 3 mood entries.
        """
        try:
            self.df = pd.read_csv('mood_data.csv')
            if len(self.df) < 3:
                print("There are less than 3 entries. Showing all available entries.")
                data_to_plot = self.df
            else:
                data_to_plot = self.df.tail(3) 

            plt.figure(figsize=(8, 6))
            sns.countplot(data=data_to_plot, x='mood', hue='severity')
            plt.title('Mood Severity Distribution for Last Entries')
            plt.xlabel('Mood')
            plt.ylabel('Count')
            plt.show()
        except FileNotFoundError:
            print("No past entries found. Please add an entry first.")
            
    def __call__(self, analysis = "summary"):
        try:
            self.df = pd.read_csv('mood_data.csv')
        except FileNotFoundError:
            return "csv file not found."
            
        if self.df.empty:
            return "No data to show."
        
        if analysis == "summary":
            return (
                f"Summary:\n"
                f"- Total Entries: {len(self.df)}\n"
                f"- Most Common Mood: {self.df['mood'].mode()[0]}\n"
                f"- Average Severity: {self.df['severity'].mean():.2f}"
            )
        elif analysis == "trend":
            mood_counts = self.df['mood'].value_counts()
            return f"mood trend: \n{mood_counts.to_string()}"
        else:
            return "Invalid analysis, use summary or trend."
        


def parse_args():
    parser = ArgumentParser(description="Mood Tracker")
    parser.add_argument('--add', action='store_true', help="Add a new mood entry")
    parser.add_argument('--view', action='store_true', help="View previous mood entries")
    parser.add_argument('--plot', action='store_true', help="Plot the last 3 mood entries")
    parser.add_argument('--analysis', type=str, help="Perform mood analysis: summary or trend")


    args = parser.parse_args()

    
    tracker = MoodTracker()

    if args.add:
        tracker.add_entry()
    elif args.view:
        tracker.view_entries()
    elif args.plot:
        tracker.plot_previous_entries()
    elif args.analysis:
        print(tracker(analysis=args.analysis))
    else:
        print("No action specified. Use add, view entries, plot, analysis.")

if __name__ == "__main__":
    parse_args()


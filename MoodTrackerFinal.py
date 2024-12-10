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
        Create a seaborn plot displaying the mood severity distribution for the last 3 mood entries.

        Attributes:
            df (pd.DataFrame): The DataFrame containing mood data read from the 'mood_data.csv' file.

        Side Effects:
            - Reads the 'mood_data.csv' file to load the mood data.
            - If there are fewer than 3 entries, all available entries will be plotted.
            - Displays a seaborn count plot showing the distribution of mood severity for the last 3 (or fewer) entries.
            - If the CSV file is not found, an error message is printed.

        Returns:
            None: The method does not return a value. It only generates and displays a plot.

        Raises:
            FileNotFoundError: If the 'mood_data.csv' file is not found.
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
        """
        Perform mood analysis on the data and return the result based on the specified analysis type.

        Args:
            analysis (str): The type of analysis to perform. 
                         Options are 'summary' or 'trend'. Default is 'summary'.
    
        Attributes:
            df (pd.DataFrame): The DataFrame containing mood data read from the 'mood_data.csv' file.

        Side Effects:
            - Reads the 'mood_data.csv' file to load the mood data.
            - If the file is not found, an error message is returned.
            - If the DataFrame is empty, an appropriate message is returned.

        Returns:
            str: A string summarizing the analysis results:
                - 'summary' analysis returns the total number of entries, the most common mood, and the average severity.
                - 'trend' analysis returns the distribution of mood counts.
                - An error message is returned if an invalid analysis type is provided or if the CSV file is not found.

        Raises:
            FileNotFoundError: If the 'mood_data.csv' file is not found.
        """
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
class Feedback(MoodTracker):
    def init(self):
        super().__init__()
    def give_feedback(self):
        feedback = []
        self.df = pd.read_csv('mood_data.csv')
    
        
        if self.df[self.df['severity']] < 3:
            feedback.append(f"THere are {len(self.df[self.df['severity']])} entries with low severity. Consider checking in with yourself to address any persistent low moods.")

        if self.df[self.df['severity'] > 8]:
            feedback.append(f"There are {len(self.df[self.df['severity']] > 8)} entries with high severity. Make sure to take care of your well-being and reach out for support if needed!.")

        sad_count = self.df[self.df['mood'] == 'sad'].shape[0]
        
        if sad_count >= 3:
            feedback.append(f"You've felt 'sad' {sad_count} times recently. It might help to talk to someone or practice self-care.")

        if feedback:
            return"\n".join(feedback)
def parse_args():
    """
    Parse command-line arguments and execute the appropriate action based on the user's input.

    Attributes:
        args (argparse.Namespace): The parsed command-line arguments containing the user's specified actions.

    Side Effects:
        - Creates an instance of the MoodTracker class.
        - Executes one of the following actions based on the parsed arguments:
          - `--add`: Adds a new mood entry by calling the `add_entry` method of the `MoodTracker` instance.
          - `--view`: Displays all previous mood entries by calling the `view_entries` method of the `MoodTracker` instance.
          - `--plot`: Plots the mood severity distribution for the last 3 entries by calling the `plot_previous_entries` method of the `MoodTracker` instance.
          - `--analysis`: Performs mood analysis (either 'summary' or 'trend') by calling the `__call__` method of the `MoodTracker` instance with the specified analysis type.

    Returns:
        None: The function does not return any value. It directly performs actions based on the command-line arguments.
    
    Raises:
        argparse.ArgumentError: If invalid arguments are passed, such as missing or incorrect flag types.
    """
    parser = ArgumentParser(description="Mood Tracker")
    parser.add_argument('--add', action='store_true', help="Add a new mood entry")
    parser.add_argument('--view', action='store_true', help="View previous mood entries")
    parser.add_argument('--plot', action='store_true', help="Plot the last 3 mood entries")
    parser.add_argument('--analysis', type=str, help="Perform mood analysis: summary or trend")
    parser.add_argument('--feedback', action='store_true', help="Get feedback on mood patterns (low/high severity or frequent sadness)")


    args = parser.parse_args()

    
    tracker = MoodTracker()
    tracker = Feedback()



    if args.feedback:
        tracker = Feedback()
        print(tracker.give_feedback())
    else:
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


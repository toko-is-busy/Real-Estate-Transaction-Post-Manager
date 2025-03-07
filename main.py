import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkcalendar import DateEntry
import pandas as pd
import os


class RealEstateApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Daily Transaction Post Manager")
        self.root.geometry("1000x600")

        # Configure style for treeview (table for displaying data)
        self.style = ttk.Style()
        self.style.configure("Treeview", rowheight=25)
        self.style.map("Treeview", background=[('selected', '#BFDBFE')])

        # Data storage for different transaction categories
        self.data = {"Ratified": pd.DataFrame(), "Sold": pd.DataFrame(), "Listed": pd.DataFrame()}

        # Notebook (tab container) for different categories
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Tabs and trees (tables) to display data for different categories
        self.tabs = {}
        self.trees = {}
        for category in ["Ratified", "Sold", "Listed"]:
            self.tabs[category] = ttk.Frame(self.notebook)
            self.notebook.add(self.tabs[category], text=category)
            self.create_tab_content(category)

        # Menu bar for exporting data
        self.menu_bar = tk.Menu(root)
        root.config(menu=self.menu_bar)

        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Export CSV", command=self.export_csv)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        # Load previously saved data when the application starts
        self.load_data()

        # Set protocol to handle window close event (save data before exiting)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_tab_content(self, category):
        # This method creates the content (Treeview, buttons) for each category tab
        frame = self.tabs[category]
        self.data[category] = pd.DataFrame(columns=["Date", "Name", "Address", "Posted"])

        # Create treeview (table) to display transaction data
        self.trees[category] = ttk.Treeview(frame, columns=("Date", "Name", "Address", "Posted"), show="headings")

        # Configure tags for coloring the rows based on posted status
        self.trees[category].tag_configure('posted', background='#baffc9')  # Soft green
        self.trees[category].tag_configure('unposted', background='#ffb3ba')  # Soft pink

        # Set up columns headers and properties
        for col in ["Date", "Name", "Address", "Posted"]:
            self.trees[category].heading(col, text=col)
            self.trees[category].column(col, width=150, anchor="w")

        # Pack the Treeview widget to fill the frame
        self.trees[category].pack(fill=tk.BOTH, expand=True)

        # Button frame for actions (Import, Delete, Mark Posted, etc.)
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=5)

        # Button actions
        ttk.Button(btn_frame, text="Import CSV", command=lambda: self.import_csv(category)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete Selected", command=lambda: self.delete_entry(category)).pack(side=tk.LEFT,
                                                                                                        padx=5)
        ttk.Button(btn_frame, text="Mark as Posted", command=lambda: self.mark_as_posted(category)).pack(side=tk.LEFT,
                                                                                                         padx=5)
        ttk.Button(btn_frame, text="Mark as Unposted", command=lambda: self.mark_as_unposted(category)).pack(
            side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Filter", command=lambda: self.filter_entries(category)).pack(side=tk.LEFT, padx=5)

        # Refresh table content
        self.refresh_table(category)

    def mark_as_posted(self, category):
        # Marks the selected items as "Posted"
        self._update_posted_status(category, True)

    def mark_as_unposted(self, category):
        # Marks the selected items as "Unposted"
        self._update_posted_status(category, False)

    def _update_posted_status(self, category, status):
        # This method updates the "Posted" status for selected entries
        selected_items = self.trees[category].selection()
        if not selected_items:
            messagebox.showwarning("Warning", "No items selected!")
            return

        for item in selected_items:
            values = self.trees[category].item(item, "values")
            mask = (
                    (self.data[category]["Date"] == values[0]) &
                    (self.data[category]["Name"] == values[1]) &
                    (self.data[category]["Address"] == values[2])
            )
            self.data[category].loc[mask, "Posted"] = status

        self.refresh_table(category)

    def delete_entry(self, category):
        # Deletes the selected entry
        selected_items = self.trees[category].selection()
        if not selected_items:
            messagebox.showwarning("Warning", "No item selected for deletion!")
            return

        for item in selected_items:
            values = self.trees[category].item(item, "values")
            mask = (
                    (self.data[category]["Date"] == values[0]) &
                    (self.data[category]["Name"] == values[1]) &
                    (self.data[category]["Address"] == values[2])
            )
            self.data[category] = self.data[category][~mask]
            self.trees[category].delete(item)

    def import_csv(self, category):
        # Imports data from a CSV file
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return

        try:
            df = pd.read_csv(file_path)
            # Mapping columns from the CSV file to internal format
            column_mapping = {
                "Listed": {"owner_name": "Name", "full_address": "Address", "listing_date": "Date"},
                "Ratified": {"owner_name": "Name", "full_address": "Address", "acceptance_date": "Date"},
                "Sold": {"owner_name": "Name", "full_address": "Address", "closing_date": "Date"}
            }

            if category in column_mapping:
                df = df.rename(columns=column_mapping[category])

                # Standardize data formats (e.g., date, strip names/addresses)
                df['Date'] = pd.to_datetime(df['Date'], errors='coerce', format='mixed').dt.strftime('%Y-%m-%d')
                df['Name'] = df['Name'].str.strip().str.title()
                df['Address'] = df['Address'].str.strip().str.title()
                df["Posted"] = False  # Only for new entries

            # Validate date column
            if df['Date'].isnull().any():
                messagebox.showwarning("Invalid Data", "Some dates could not be parsed. Please check your CSV format.")
                return

            # Check for required columns in the CSV file
            required_columns = ["Date", "Name", "Address", "Posted"]
            if not all(col in df.columns for col in required_columns):
                messagebox.showerror("Error", "CSV file is missing required columns")
                return

            # Merge new data with existing data and remove duplicates
            existing_df = self.data[category].copy()
            existing_df['Date'] = pd.to_datetime(existing_df['Date'], errors='coerce').dt.strftime('%Y-%m-%d')
            existing_df['Name'] = existing_df['Name'].str.strip().str.title()
            existing_df['Address'] = existing_df['Address'].str.strip().str.title()

            merged_df = pd.concat([existing_df, df[required_columns]])
            merged_df = merged_df.drop_duplicates(subset=["Date", "Name", "Address"], keep='first')

            self.data[category] = merged_df
            self.refresh_table(category)

        except Exception as e:
            messagebox.showerror("Import Error", f"Failed to import CSV: {str(e)}")

    def filter_entries(self, category):
        # Opens a filter dialog for filtering data by date range, name, and posted status
        filter_dialog = tk.Toplevel(self.root)
        filter_dialog.title("Filter Options")
        filter_dialog.transient(self.root)
        filter_dialog.grab_set()

        # Create UI elements for filter options (date, name, posted status)
        ttk.Label(filter_dialog, text="Start Date:").grid(row=0, column=0, padx=5, pady=5)
        start_date_entry = DateEntry(filter_dialog)
        start_date_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(filter_dialog, text="End Date:").grid(row=1, column=0, padx=5, pady=5)
        end_date_entry = DateEntry(filter_dialog)
        end_date_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(filter_dialog, text="Name Contains:").grid(row=2, column=0, padx=5, pady=5)
        name_entry = ttk.Entry(filter_dialog)
        name_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(filter_dialog, text="Posted Status:").grid(row=3, column=0, padx=5, pady=5)
        posted_var = tk.StringVar(value="All")
        ttk.Combobox(filter_dialog, textvariable=posted_var,
                     values=["All", "Posted", "Unposted"], state="readonly").grid(row=3, column=1, padx=5, pady=5)

        def apply_filter():
            # Applies the selected filters and refreshes the table
            try:
                start_date = start_date_entry.get_date()
                end_date = end_date_entry.get_date()
                name_filter = name_entry.get().strip()
                posted_filter = posted_var.get()

                filtered_data = self.data[category].copy()
                filtered_data['Date'] = pd.to_datetime(filtered_data['Date'])

                # Date filter
                if start_date and end_date:
                    filtered_data = filtered_data[
                        (filtered_data['Date'] >= pd.to_datetime(start_date)) &
                        (filtered_data['Date'] <= pd.to_datetime(end_date))
                        ]

                # Name filter
                if name_filter:
                    filtered_data = filtered_data[
                        filtered_data['Name'].str.contains(name_filter, case=False, na=False)
                    ]

                # Status filter
                if posted_filter == "Posted":
                    filtered_data = filtered_data[filtered_data['Posted']]
                elif posted_filter == "Unposted":
                    filtered_data = filtered_data[~filtered_data['Posted']]

                self.refresh_table(category, filtered_data)
                filter_dialog.destroy()

            except Exception as e:
                messagebox.showerror("Filter Error", f"Invalid filter parameters: {str(e)}")

        ttk.Button(filter_dialog, text="Apply Filter", command=apply_filter).grid(row=4, columnspan=2, pady=10)

    def refresh_table(self, category, filtered_data=None):
        # Refreshes the table content based on filtered data
        tree = self.trees[category]
        tree.delete(*tree.get_children())

        data_to_display = filtered_data if filtered_data is not None else self.data[category]
        for _, row in data_to_display.iterrows():
            posted_status = "Yes" if row["Posted"] else "No"
            tag = 'posted' if row["Posted"] else 'unposted'

            tree.insert("", tk.END,
                        values=(
                            row["Date"].strftime('%Y-%m-%d') if isinstance(row["Date"], pd.Timestamp) else row["Date"],
                            row["Name"],
                            row["Address"],
                            posted_status
                        ),
                        tags=(tag,))

    def load_data(self):
        # Loads data from CSV files for each category (Ratified, Sold, Listed)
        for category in self.data:
            try:
                df = pd.read_csv(f"{category}.csv")
                df['Posted'] = df['Posted'].astype(bool)
                df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
                self.data[category] = df
                self.refresh_table(category)
            except FileNotFoundError:
                pass
            except Exception as e:
                messagebox.showerror("Load Error", f"Error loading {category}.csv: {str(e)}")

    def save_data(self):
        # Saves data to CSV files for each category (Ratified, Sold, Listed)
        for category in self.data:
            try:
                self.data[category].to_csv(f"{category}.csv", index=False)
            except Exception as e:
                messagebox.showerror("Save Error", f"Error saving {category}.csv: {str(e)}")

    def export_csv(self):
        # Exports all categories' data into a single CSV file
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return

        try:
            combined_df = pd.concat(self.data.values())
            combined_df.to_csv(file_path, index=False)
            messagebox.showinfo("Export", "Data exported successfully!")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export data: {str(e)}")

    def on_close(self):
        # Save data before closing the application
        self.save_data()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = RealEstateApp(root)
    root.mainloop()

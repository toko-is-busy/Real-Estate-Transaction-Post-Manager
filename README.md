# 🏡 Daily Transaction Post Manager

**Daily Transaction Post Manager** is a Python-based GUI application that helps manage real estate transactions categorized under **Ratified, Sold, and Listed**. It allows users to **import, filter, mark, and export transactions** with ease. This is specifically made by a social media manager of a Brokerage that constantly cross-checks the list if the transaction was posted. This will make sure that any and all transaction will not be duplicated as long as it already exists in the dataframe under the category. 

## 📌 Features
- **Three Tabs:** `Ratified`, `Sold`, and `Listed` to categorize transactions.
- **CSV Import Support:** Imports transaction data from CSV files.
- **Interactive Table:** Allows marking transactions as `Posted` with checkboxes.
- **Filtering Options:** Filter by date, name, and posted status.
- **Delete Functionality:** Select and remove specific transactions.
- **Export Transactions:** Save all transaction data to a CSV file.
- **Deletes Duplicates:** Any duplicates that appear in your CSV that is already in the dataframe will be ignored. 

---

## 🛠️ Installation

### 1️⃣ Install Python (if not installed)
Ensure you have **Python 3.8+** installed.  
Download it from [Python.org](https://www.python.org/downloads/).

### 2️⃣ Install Required Dependencies
Run the following command in your terminal or command prompt:

```sh
pip install pandas tkcalendar
```

---

## 📂 CSV Format Requirements

To correctly import transactions, your CSV files must follow the required column names per category:

### **Listed.csv**
| listing_date | owner_name | full_address |
|-------------|------------|-------------|
| 2025-03-01 | John Doe | 123 Main St, City, ST 12345 |

### **Ratified.csv**
| acceptance_date | owner_name | full_address |
|----------------|------------|-------------|
| 2025-03-02 | Jane Doe | 456 Oak St, City, ST 67890 |

### **Sold.csv**
| closing_date | owner_name | full_address |
|-------------|------------|-------------|
| 2025-03-03 | Mike Smith | 789 Pine St, City, ST 54321 |

⚠️ **Note:** The application automatically renames the headers to:
- `Date`
- `Name`
- `Address`
- `Posted` (automatically set to `False` on import)

---

## 🚀 Usage

### **Run the Application**
To start the application, open a terminal or command prompt and run:

```sh
python main.py
```

### **Importing a CSV**
1. Select a category tab (`Ratified`, `Sold`, `Listed`).
2. Click the **"Import CSV"** button.
3. Choose a CSV file that follows the correct format.

### **Marking as Posted**
- Click on the **checkbox** in the "Posted" column to toggle its status.

### **Deleting Transactions**
- Select a row and click **"Delete Selected"** to remove it.

### **Filtering Transactions**
- Click **"Filter"** and set the desired criteria.

### **Exporting Data**
- Click **"File" > "Export CSV"** to save all transactions.

---

## 🔧 Troubleshooting
If you encounter issues:
- **Check your CSV file formatting.**
- **Ensure all required Python libraries are installed** (`pandas`, `tkcalendar`).
- **Use Python 3.8+** for best compatibility.

---

## 📜 License
This project is **open-source** and free to use.

---

✅ **Enjoy using the Daily Transaction Post Manager!**

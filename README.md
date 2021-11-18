# Scripts

## About the repository
The repository contains useful scripts written using sh
## How to set up?
1. Git clone
2. Give permissions to your file by type the command *chmod +x {your_script_name}*

## What can do the scripts?

1. **call_list_generator.sh**<br>
- Creates desired amount of records inside the new txt file <br>
- Run the script by typing *./call_list_generator.sh*
- You can declare your *DEF_COUNRY_CODE* and *AMOUNT_OF_RECORDS* by opening the file<br>
<br>  New created call list *calling_list1000.txt* contains:
```Account, Name, Phone number
0, name, 10 
1, name, 11 
2, name, 12 
3, name, 13 
4, name, 14 
5, name, 15 
6, name, 16 
7, name, 17 
8, name, 18
... 
```
2. **fresh_log_zipper.sh**<br>
- Takes fresh logs without numbers prefix
- Compresses their as zip archive <br>
- Run the script by typing *./fresh_log_zipper {name_of_your_atchive.zip}*
- You can declare a custom directory where the script can find logs by changing the *LOG_FOLDER* inside the file
3. **make_file_size.sh**
- Updates file to a specific size
- By default, the size is 38000000 KB
- You can set up custom size by changing the value twice inside the script
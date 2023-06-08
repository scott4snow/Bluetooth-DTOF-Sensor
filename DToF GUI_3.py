import asyncio
import tkinter as tk
from bleak import BleakClient, discover

# Define the characteristic UUID of the BLE device
# Replace with your characteristic UUID
uuid = "19B10001-E8F2-537E-4F6C-D104768A1214"

# Define an async function that reads the hex value from the characteristic and converts it to decimal


async def read_hex(client):
    data = await client.read_gatt_char(uuid)  # Read the data as bytes
    hex_value = data.hex()  # Convert the bytes to hex string
    dec_value = int(hex_value, 16)  # Convert the hex string to decimal integer
    return dec_value

# Define a normal function that updates the GUI label with the decimal value


def update_label(label, loop):
    async def get_value():
        async with BleakClient(address) as client:  # Connect to the BLE device
            # Get the decimal value from the characteristic
            value = await read_hex(client)
            # Update the label text with the value
            label.config(text=str(value))
    # Create an asyncio task to run the async function
    loop.create_task(get_value())

# Define a normal function that disconnects from the BLE device


def disconnect(loop):
    async def close_connection():
        # Create a bleak client object with the address
        client = BleakClient(address)
        await client.disconnect()  # Disconnect from the BLE device
    # Create an asyncio task to run the async function
    loop.create_task(close_connection())

# Define an async function that scans for nearby BLE devices and returns a list of their addresses and names


async def scan(listbox):
    # Clear the listbox
    listbox.delete(0, tk.END)
    # Create a BleakScanner object
    scanner = bleak.BleakScanner()
    # Start scanning for 2 seconds
    await scanner.start()
    await asyncio.sleep(2)
    await scanner.stop()
    # Get the scanned devices
    devices = await scanner.get_discovered_devices()
    # Loop through the devices and add them to the listbox
    for d in devices:
        listbox.insert(tk.END, f"{d.name} - {d.address}")

# Define a normal function that updates the GUI listbox with the scanned devices


# Define a normal function that updates the GUI listbox with the scanned devices
def update_listbox(listbox, loop):
    async def get_devices():
        devices = await scan(listbox)  # Use the await keyword here
        # The rest of the code is unchanged
        listbox.delete(0, tk.END)  # Delete all items in the listbox
        for d in devices:  # Loop through each device
            # Insert an item with the address and name of the device
            listbox.insert(tk.END, f"{d[0]} - {d[1]}")
    # Create an asyncio task to run the async function
    loop.create_task(get_devices())


# Define a global variable for the address of the selected device
address = None

# Define a normal function that sets the address of the selected device from the listbox


def select_device(listbox):
    global address  # Use the global variable address
    # Get the index of the selected item in the listbox
    selection = listbox.curselection()
    if selection:  # If there is a selection
        item = listbox.get(selection[0])  # Get the item text from the listbox
        # Split the item text by " - " and get the first part as the address
        address = item.split(" - ")[0]

# Define a normal function that creates and starts the GUI


def start_gui(loop):
    root = tk.Tk()  # Create a root window
    label = tk.Label(root)  # Create a label widget
    label.pack()  # Pack the label widget into the root window
    # Create a button widget that calls the update_label function when clicked
    button1 = tk.Button(root, text="Read",
                        command=lambda: update_label(label, loop))

    button1.pack()  # Pack the button widget into the root window
    # Create another button widget that calls the disconnect function when clicked
    button2 = tk.Button(root, text="Disconnect",
                        command=lambda: disconnect(loop))
    button2.pack()  # Pack the button widget into the root window
    # Create a listbox to display the devices
    # global listbox
    listbox = tk.Listbox(root)
    listbox.pack()

    # Create another button widget that calls the update_listbox function when clicked
    button3 = tk.Button(root, text="Scan",
                        command=lambda: scan(listbox))
    button3.pack()  # Pack the button widget into the root window
    # Create another button widget that calls the select_device function when clicked
    button4 = tk.Button(root, text="Connect",
                        command=lambda: select_device(listbox))
    button4.pack()  # Pack the button widget into the root window
    root.mainloop()  # Start the tkinter main loop


loop = asyncio.get_event_loop()  # Get the asyncio event loop
start_gui(loop)  # Call the start_gui function with the loop

import sys
import time
from multiprocessing import Process


def spinning_cursor():
    """
        Generator Method to infinitely display a cursor in different position for spinner.
    """
    # List (of characters) of Cursor Symbols.
    # Cursor Symbols for all the directions
    cursors = '|/-\\'

    # Infinetely yield the next cursor symbol for spinner
    while True:
        for cursor in cursors:
            yield cursor


def spin_infinite(delay=.1, message=''):
    """
    Display Spinner for a infinite number of time

    Parameters:
    ---
    delay: number
        No of seconds the cursor should remain in one direction        
    msg: str
        Message that should get logged along with the spinner
    """
    # Get the generator object to iterate over the cursor symbols infinetely
    spinner = spinning_cursor()
    # Manually Add a new line
    print()
    # Display the Message
    # Set end = ' ', to avoid new line (& to just leave a space).  So, that the spinner will appear in the same line
    print(message.strip(), end=' ')

    # Iterate over the infinite spinner generator object
    for cursor in spinner:
        # Print the correct cursor for the current direction
        # Set end='' to avoid new line
        print(cursor, end='')
        # Delay (i.e., Pause) the spinner
        time.sleep(delay)
        # Python's standard out is buffered by default
        # Since we sleep for some time after the printing, Python won't print the cursor (of the previous line print(...)) immediately, instead it will wait for some time to print even after sleeping
        # The data that we printed in the previous line will go the buffer memory, instead of displaying in the standard output
        # The below sys.stdout.flush() will force the Python to "flush" the buffer (& write that data to the std output (i.e., Terminal))
        sys.stdout.flush()
        # Remove the Cursor for the previous direction
        # Set end='' to avoid new line
        print('\b', end='')


def spin(count=20, delay=.1, message=''):
    """
    Display Spinner until a specific count

    Parameters:
    ---
    count: number 
        Number of iteration, the spinner should take to complete the spinning
    delay: number
        No of seconds the cursor should remain in one direction        
    msg: str
        Message that should get logged along with the spinner
    """
    # Get the generator object to iterate over the cursor symbols
    spinner = spinning_cursor()
    # Manually Add a new line
    print()
    # Display the Message & Prevent the new line at the end of the print (end = ' ')
    print(message.strip(), end=' ')

    # Spin until the count
    for _ in range(count):
        # Print the correct cursor for the current direction & Prevent the new line being added (end = '')
        print(next(spinner), end='')
        # Delay (i.e., Pause) the spinner
        time.sleep(delay)
        # Since we pause the execution, Python's standard out is buffered by default
        # sys.stdout.flush() will force the Python to "flush" the buffer
        sys.stdout.flush()
        # Remove the previous cursor & Prevent the new line being added (end = '')
        print('\b', end='')


def spin(count=20, delay=.1, message=''):
    """
        Display Spinner until a specific count

        count => Number (in number) of iteration, the spinner should take to complete the spinning
        delay => Seconds (in number) in which the cursor direction should change.  Default value is .1 (100 milli-seconds)
        message => Message (string) that should display along with the spinner.  Default value is an empty string
    """
    # Get the generator object to iterate over the cursor symbols
    spinner = spinning_cursor()
    # Display the Message & Prevent the new line at the end of the print (end = ' ')
    print(message.strip(), end=' ')

    # Spin until the count
    for _ in range(count):
        # Print the correct cursor for the current direction & Prevent the new line being added (end = '')
        print(next(spinner), end='')
        # Delay (i.e., Pause) the spinner
        time.sleep(delay)
        # Since we pause the execution, Python's standard out is buffered by default
        # sys.stdout.flush() will force the Python to "flush" the buffer
        sys.stdout.flush()
        # Remove the previous cursor & Prevent the new line being added (end = '')
        print('\b', end='')


def start_spinner(delay=.5, msg='PROCESSING', count=-1):
    """
    Uses spinner package to display spinner parallely

    Parameters:
    ---
    delay: number
        No of seconds the cursor should remain in one direction        
    msg: str
        Message that should get logged along with the spinner
    count: number
        If -1, then spin for infinite no of times, else spin for count no of times(default -1)
    """
    try:
        # Created a new process to display spinner asynchronously
        if count == -1:
            spnr = Process(target=spin_infinite, args=(delay, msg))
        else:
            spnr = Process(target=spin, args=(count, delay, msg))
        # Start Spinning
        spnr.start()
        return spnr
    except:
        print('Unable to Start a Spinner')


def stop_spinner(spnr: Process, msg="done"):
    """
    Terminate the spinner process

    Parameters:
    ---
    spnr: Process
        Instance of the running spinner process
    msg: str
        Stop Message
    """
    try:
        # Stop Spinning
        spnr.terminate()
        print("")
        print(msg)
    except:
        print('Unable to Stop the Spinner')


if __name__ == '__main__':
    spin(4)

if __name__ == '__main__':
    spin(4)

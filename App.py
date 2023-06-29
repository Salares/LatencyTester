import subprocess
import re
import time
import wandb

# Initialize Weights & Biases
wandb.login()
wandb.init(project="latency-monitor")

# Define the destination address to ping
destination_address = "8.8.8.8"  # Example: Google's DNS server
previous_latency = 0
time_spent = 0

# Continuously ping the destination and log the latency
start = time.time()

while True:
    try:
        # Execute the ping command and capture the output
        output = subprocess.check_output(['ping', '-n', '1', '-w', '200', destination_address], universal_newlines=True)

        # Extract the average round-trip time (latency) from the ping output
        latency = re.findall(r"Average = (\d+)", output)
        if latency:
            latency = int(latency[0])
        else:
            latency = -1
        
        if previous_latency == 0:
            previous_latency = latency

        time_spent = (time.time() - start) * 1000

        # Log the latency to Weights & Biases
        if previous_latency != -1:
            wandb.log({"Quotient":float(previous_latency) / float(latency)}, step=int(time_spent))
            # print({"Quotient":float(previous_latency) / float(latency)})
            previous_latency = latency
        wandb.log({"Latency": latency}, step=int(time_spent))
        print({"Latency": latency})

    except subprocess.CalledProcessError:
        # Handle any errors that occur during the ping command
        latency = -1
        wandb.log({"Latency": latency}, step=int(time_spent))
        # print({"Latency": latency}, step=time_spent)

    # Sleep for a specific interval before pinging again
    time.sleep(0.25)  # Adjust this value as needed
    
    # print(time_spent)

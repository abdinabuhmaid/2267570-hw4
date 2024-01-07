# Task-1: Construct a list of dictionaries by importing hirstorical data from the file orcl.csv
def load_data(file_path):
    data = []
    with open(file_path, 'r') as file:
        # Inspect the lines listed in the file
        lines = file.readlines()
        # Retrieve the headers from the given line
        headers = lines[0].strip().split(',')
        # Create a loop through the remaining lines and construct dictionaries
        for line in lines[1:]:
            values = line.strip().split(',')
            entry = dict(zip(headers, values))
            data.append(entry)
   # return the value data
    return data

# Task-2: Evaluate the Simple Moving Averages(SMA) and Relative Strength Index(RSI)
def calculate_indicators(data):
    sma_values = []
    rsi_values = []
    # construct a loop to calculate the Simple Moving Averages (SMA) for each point
    for i in range(len(data)):
        # Compute the Simple Moving Averages (SMA)
        if i >= 4:  # Need at least 5 days for a 5-day SMA
            close_prices = [float(data[j]['Close']) for j in range(i-4, i+1)]
            sma = sum(close_prices) / 5
            sma_values.append({'Date': data[i]['Date'], 'SMA': sma})

        # Evaluate Relative Strength Index (RSI)
        if i >= 13:  # Need at least 14 days for a 14-day RSI
            gains = losses = 0
            for j in range(i-13, i):
                price_change = float(data[j+1]['Close']) - float(data[j]['Close'])
                if price_change > 0:
                    gains += price_change
                else:
                    losses += abs(price_change)

            avg_gain = (gains + float(data[i]['Close']) - float(data[i-13]['Close'])) / 14
            avg_loss = (losses + abs(float(data[i]['Close']) - float(data[i-13]['Close']))) / 14
            # In order to evade the possibility of division by zero
            if avg_loss == 0:
                rsi = 100
            else:
                rs = avg_gain / avg_loss
                rsi = 100 - (100 / (1 + rs))

            rsi_values.append({'Date': data[i]['Date'], 'RSI': rsi})
    # return the values for sma_values and rsi_values
    return sma_values, rsi_values


# Task-3: Store the indicators to files
def write_to_file(data, file_path):
    with open(file_path, 'w') as file:
        # Store the headers to the file given
        headers = ','.join(data[0].keys())
        file.write(headers + '\n')
        # Store the data to the file given
        for entry in data:
            values = ','.join(map(str, entry.values()))
            file.write(values + '\n')

# Retrieve the data from a CSV file
file_path = "orcl.csv"
historical_data = load_data(file_path)

# Evaluate the indicators
sma_values, rsi_values = calculate_indicators(historical_data)

# Store the indicators in files
write_to_file(sma_values, "orcl-sma.csv")
write_to_file(rsi_values, "orcl-rsi.csv")



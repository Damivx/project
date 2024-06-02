class Logger:
    def __init__(self, filename):
        self.filename = filename

    def log(self, message):
        with open(self.filename, 'a') as f:
            f.write(message + "\n")

# Example usage
if __name__ == "__main__":
    logger = Logger("scan_results.txt")
    logger.log("Scan started for http://example.com")


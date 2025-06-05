import logfire

# Configure Logfire
logfire.configure()

# Log a message
logfire.info("Hello {place}", place="world")

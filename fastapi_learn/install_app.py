import subprocess

def run_command(command, check=True):
    """Helper function to run a shell command."""
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    if check and result.returncode != 0:
        raise Exception(f"Command failed: {result.stderr}")
    return result.stdout

def install_postgresql():
    """Install PostgreSQL on Ubuntu."""
    try:
        # Update package list
        print("Updating package list...")
        run_command("sudo apt update")

        # Install PostgreSQL
        print("Installing PostgreSQL...")
        run_command("sudo apt install -y postgresql postgresql-contrib")

        # Start PostgreSQL service
        print("Starting PostgreSQL service...")
        run_command("sudo systemctl start postgresql")

        # Enable PostgreSQL to start on boot
        print("Enabling PostgreSQL service to start on boot...")
        run_command("sudo systemctl enable postgresql")

        print("PostgreSQL installed and running.")
    except Exception as e:
        print(f"Error during installation: {e}")

def setup_database():
    """Setup a new PostgreSQL database and user."""
    try:
        # Create a PostgreSQL user and database
        print("Creating PostgreSQL user and database...")
        run_command("sudo -u postgres psql -c \"CREATE USER myuser WITH PASSWORD 'mypassword';\"")
        run_command("sudo -u postgres psql -c \"CREATE DATABASE mydb OWNER myuser;\"")

        print("Database 'mydb' and user 'myuser' created.")
    except Exception as e:
        print(f"Error during database setup: {e}")

if __name__ == "__main__":
    install_postgresql()
    setup_database()

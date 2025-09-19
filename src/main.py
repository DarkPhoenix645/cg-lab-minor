from gui import GUI

def main():
    try:
        app = GUI(width=1024, height=768)
        app.run()
    except KeyboardInterrupt:
        print("\n")
        print("Application interrupted by user")
    except Exception as e:
        print(f"An error occurred: {e}")
        return 1
    return 0

if __name__ == "__main__":
    exit(main())

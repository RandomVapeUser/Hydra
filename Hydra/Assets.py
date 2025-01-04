from rgbprint import gradient_print, Color

class AsciiAssets:
    """Global Ascii text and utility methods for the Multitool."""
    start_color = 0x4BBEE3
    end_color = Color.medium_violet_red

    main_text = [
        """

        | [<<] @~> Back                    
        |
        | [01] @~> Channel Spammer      [05] @~> Formater            [9] @~> Nickname Changer
        | [02] @~> Server Joiner        [06] @~> Server Checker
        | [03] @~> Token Checker        [07] @~> Member Scraper
        | [04] @~> Accept Rules         [08] @~> Bio Changer
        |
        | Choose >>: """,
        """

        | [<<] @~> Back                    
        |
        | [01] @~> Webhook Spammer
        | [02] @~> Webhook Name Changer
        | [03] @~> Webhook Deleter
        | [04] @~> Webhook Info
        |
        | Choose >>: """,
        """

        | [<<] @~> Back                    
        |
        | [01] @~> Group Chat Name Changer Spammer
        | [02] @~> Server Invite Info
        | [03] @~> Dm Spammer
        |
        | Choose >>: """,

        """

        | [<<] Back                    
        |
        | [1] - Theme
        |
        | Choose >>: """,

        """
        | Themes                   
        |
        | [1] - Default (Violet Purple)
        | [2] - Red
        | [3] - Blue
        | [4] - Orange
        | 
        | Choose >>: """,
        """

        | [<<] Back                    
        |
        | Main Dev - Sal (salomao31v2)
        |
        | Choose >>: """,
        """
        | [XX] @~> Exit
        
        | [01] >>> Webhook Modules
        | [02] >>> Token Modules
        | [03] >>> Other Modules
        | [04] >>> Settings
        | [05] >>> Credits
        
        | Choose >>: """
    ]

    #Hydra Logo
    def send_logo(self):
        """Display the logo with gradient text."""
        gradient_print("""
                     _   _           _            ___  ___      _ _   _ _              _ 
                    | | | |         | |           |  \/  |     | | | (_) |            | |
                    | |_| |_   _  __| |_ __ __ _  | .  . |_   _| | |_ _| |_ ___   ___ | |
                    |  _  | | | |/ _` | '__/ _` | | |\/| | | | | | __| | __/ _ \ / _ \| |
                    | | | | |_| | (_| | | | (_| | | |  | | |_| | | |_| | || (_) | (_) | |
                    \_| |_/\__, |\__,_|_|  \__,_| \_|  |_/\__,_|_|\__|_|\__\___/ \___/|_|
                            __/ |                                                         
                           |___/                                                          
        """, start_color=AsciiAssets.start_color, end_color=AsciiAssets.end_color)

    #Set color theme    
    def set_theme(theme):
        """Set color theme for ASCII art."""
        match theme:
            case "DEFAULT":
                AsciiAssets.start_color = 0x4BBEE3
                AsciiAssets.end_color = Color.medium_violet_red
            case "BLUE":
                AsciiAssets.start_color = 0x4BBEE3
                AsciiAssets.end_color = Color.medium_aqua_marine
            case "RED":
                AsciiAssets.start_color = 0xFF6347
                AsciiAssets.end_color = Color.dark_red
            case "ORANGE": 
                AsciiAssets.start_color = 0xFFA500
                AsciiAssets.end_color = Color.orange_red
            case _:
                AsciiAssets.start_color = 0x4BBEE3
                AsciiAssets.end_color = Color.medium_violet_red

    #Custom message display
    @staticmethod
    def cmessage(content, trigger=False):
        """Custom message display using gradient print."""
        if trigger:
            gradient_print(
                f"{content}", 
                start_color=AsciiAssets.start_color, 
                end_color=AsciiAssets.end_color,
                end=""
            )
        else:
            gradient_print(
                f"{content}", 
                start_color=AsciiAssets.start_color, 
                end_color=AsciiAssets.end_color
            )

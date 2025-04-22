# menus.py
# Author: Max Weber, Mojtaba Malek-Nejad
# if you want to see more detailed information about the individual contributors of the code files, 
# please have a look at the "contributors.txt" file (in the "project" directory)

import pygame as pg
from .menu_ui import MenuUI
from .menu_state import MenuState
from utils.path_utils import PathUtils
import os
from ui.font_manager import FontManager

class GameMenus:
    def __init__(self, width, height, surface):
        self.width = width
        self.height = height
        self.surface = surface
        self.ui = MenuUI(width, height)
        self.state = MenuState()
        self.demo_selected = False  # Add selected state for demo button
        self.font_manager = FontManager()  # Initialize FontManager
        
        # Hintergrund laden - verwende das vorhandene Menü-Hintergrundbild
        pathutil = PathUtils()
        menu_bg_path = pathutil.get_image_path('start_menu_background_wood.png')
        self.menu_background = pg.image.load(menu_bg_path)
        self.menu_background = pg.transform.scale(self.menu_background, (width, height))
        
        # Cache für Teammitglieder-Bilder
        self.team_images_cache = {}

    def apply_rounded_corners(self, image, radius):
        """Apply rounded corners to an image surface"""
        rect = image.get_rect()
        
        # Create a new surface with alpha channel
        rounded = pg.Surface(rect.size, pg.SRCALPHA)
        
        # Draw the rounded rectangle mask
        pg.draw.rect(rounded, (255, 255, 255, 255), rect, border_radius=radius)
        
        # Blit the original image onto the mask
        rounded.blit(image, (0, 0), special_flags=pg.BLEND_RGBA_MIN)
        
        return rounded

    def draw_main_menu(self):
        # Draw background
        self.surface.blit(self.menu_background, (0, 0))
        
        # Menu buttons (calculate button dimensions first to use for title positioning)
        button_font = self.ui.get_button_font(self.height // 20)
        button_y_start = self.height // 2 - 100
        button_spacing = 70
        button_x = 40
        
        button_texts = ["Start Game (Enter)", "Change Mode", "Change Difficulty", "About Us", "Quit Game"]
        button_width = self.ui.get_max_button_width(button_texts, button_font)
        button_height = button_font.get_height() + 20  # Move this up with other button calculations
        
        # Calculate center position for titles (same as button center)
        title_x = button_x + (button_width // 2)
        title_offset = int(button_height * 0.80)  # 80% of button height as constant offset
        
        # Title with outline and shadow (using Anirb font)
        title_font = self.font_manager.get_title_font(int(self.height / 2.4))  # Make the font slightly smaller
        subtitle_font = self.font_manager.get_title_font(int(self.height / 4.2))  # Make subtitle even smaller
        
        # Draw main title
        self.ui.draw_text_with_outline(
            self.surface,
            "LingoGuess",
            title_font,
            (255, 255, 255),
            title_x,  # Use calculated x position
            self.height // 7.5 + title_offset,  # Move down by offset
            outline_width=3
        )
        
        # Draw subtitle
        self.ui.draw_text_with_outline(
            self.surface,
            "A Hero's Quest",
            subtitle_font,
            (255, 255, 255),
            title_x,  # Use same x position for subtitle
            self.height // 5 + title_offset,  # Move down by same offset
            outline_width=3
        )
        
        buttons = []
        mouse_pos = pg.mouse.get_pos()
        
        for i, text in enumerate(button_texts):
            button_rect = pg.Rect(button_x, button_y_start + i * button_spacing, button_width, button_height)
            is_hovered = button_rect.collidepoint(mouse_pos)
            
            rect = self.ui.draw_stone_button(
                self.surface,
                text,
                button_font,
                button_x,
                button_y_start + i * button_spacing,
                button_width,
                button_height,
                False,  # is_selected
                is_hovered
            )
            buttons.append((text, rect))
        
        return buttons

    def draw_mode_menu(self):
        # Draw background
        self.surface.blit(self.menu_background, (0, 0))
        
        # Menu buttons (calculate button dimensions first to use for title positioning)
        button_font = self.ui.get_button_font(self.height // 20)
        button_y_start = self.height // 2 - 100
        button_spacing = 70
        button_x = 40
        button_height = button_font.get_height() + 20
        
        # Calculate widths for mode buttons and control buttons separately
        mode_button_width = self.ui.get_max_button_width(self.state.modes, button_font)
        control_button_width = self.ui.get_max_button_width(["Apply and go back", "Cancel and go back"], button_font)
        max_button_width = max(mode_button_width, control_button_width)
        
        # Calculate title position to match main menu
        title_x = button_x + (max_button_width // 2)
        title_offset = int(button_height * 0.80)
        
        # Title with outline
        title_font = self.font_manager.get_submenu_font(int(self.height / 4))  # Using submenu font with appropriate size
        self.ui.draw_text_with_outline(
            self.surface,
            "Select Mode",
            title_font,
            (255, 255, 255),
            title_x,
            self.height // 7.5 + title_offset,
            outline_width=3
        )
        
        buttons = []
        mouse_pos = pg.mouse.get_pos()
        
        # Mode buttons
        for i, mode in enumerate(self.state.modes):
            button_rect = pg.Rect(button_x, button_y_start + i * button_spacing, mode_button_width, button_height)
            is_hovered = button_rect.collidepoint(mouse_pos)
            
            rect = self.ui.draw_stone_button(
                self.surface,
                mode,
                button_font,
                button_x,
                button_y_start + i * button_spacing,
                mode_button_width,
                button_height,
                mode == self.state.temp_mode,
                is_hovered
            )
            buttons.append((mode, rect))
        
        # Control buttons
        y_offset = button_y_start + len(self.state.modes) * button_spacing + 20
        
        # Apply button
        apply_rect_bounds = pg.Rect(button_x, y_offset, control_button_width, button_height)
        is_apply_hovered = apply_rect_bounds.collidepoint(mouse_pos)
        apply_rect = self.ui.draw_stone_button(
            self.surface,
            "Apply and go back",
            button_font,
            button_x,
            y_offset,
            control_button_width,
            button_height,
            False,
            is_apply_hovered
        )
        
        # Cancel button
        cancel_rect_bounds = pg.Rect(button_x, y_offset + button_spacing, control_button_width, button_height)
        is_cancel_hovered = cancel_rect_bounds.collidepoint(mouse_pos)
        cancel_rect = self.ui.draw_stone_button(
            self.surface,
            "Cancel and go back",
            button_font,
            button_x,
            y_offset + button_spacing,
            control_button_width,
            button_height,
            False,
            is_cancel_hovered
        )
        
        buttons.extend([("Apply and go back", apply_rect), ("Cancel and go back", cancel_rect)])
        return buttons

    def draw_difficulty_menu(self):
        # Draw background
        self.surface.blit(self.menu_background, (0, 0))
        
        # Menu buttons (calculate button dimensions first to use for title positioning)
        button_font = self.ui.get_button_font(self.height // 20)
        button_y_start = self.height // 2 - 130  # Moved up slightly from -100
        button_spacing = 55  # Keep the tighter spacing for difficulty buttons
        button_x = 40
        
        # Different heights for difficulty buttons and control buttons
        diff_button_height = button_font.get_height() + 15  # Keep the smaller height for difficulty buttons
        control_button_height = button_font.get_height() + 20  # Restore original height for control buttons
        
        # Calculate widths for difficulty buttons and control buttons separately
        diff_button_width = self.ui.get_max_button_width(self.state.difficulties, button_font)
        control_button_width = self.ui.get_max_button_width(["Apply and go back", "Cancel and go back"], button_font)
        max_button_width = max(diff_button_width, control_button_width)
        
        # Calculate title position to match main menu
        title_x = button_x + (max_button_width // 2)
        title_offset = int(diff_button_height * 0.80)
        
        # Title with outline
        title_font = self.font_manager.get_submenu_font(int(self.height / 5.0))  # Smaller size specifically for difficulty menu
        self.ui.draw_text_with_outline(
            self.surface,
            "Select Difficulty",
            title_font,
            (255, 255, 255),
            title_x,
            self.height // 7.5 + title_offset,
            outline_width=3
        )
        
        buttons = []
        mouse_pos = pg.mouse.get_pos()
        
        # Difficulty buttons
        for i, diff in enumerate(self.state.difficulties):
            button_rect = pg.Rect(button_x, button_y_start + i * button_spacing, diff_button_width, diff_button_height)
            is_hovered = button_rect.collidepoint(mouse_pos)
            
            rect = self.ui.draw_stone_button(
                self.surface,
                diff,
                button_font,
                button_x,
                button_y_start + i * button_spacing,
                diff_button_width,
                diff_button_height,
                diff == self.state.temp_difficulty,
                is_hovered
            )
            buttons.append((diff, rect))
        
        # Control buttons with original spacing and height
        control_spacing = 70  # Restore original spacing for control buttons
        y_offset = button_y_start + len(self.state.difficulties) * button_spacing + 30  # Slightly larger gap
        
        # Apply button
        apply_rect_bounds = pg.Rect(button_x, y_offset, control_button_width, control_button_height)
        is_apply_hovered = apply_rect_bounds.collidepoint(mouse_pos)
        apply_rect = self.ui.draw_stone_button(
            self.surface,
            "Apply and go back",
            button_font,
            button_x,
            y_offset,
            control_button_width,
            control_button_height,
            False,
            is_apply_hovered
        )
        
        # Cancel button
        cancel_rect_bounds = pg.Rect(button_x, y_offset + control_spacing, control_button_width, control_button_height)
        is_cancel_hovered = cancel_rect_bounds.collidepoint(mouse_pos)
        cancel_rect = self.ui.draw_stone_button(
            self.surface,
            "Cancel and go back",
            button_font,
            button_x,
            y_offset + control_spacing,
            control_button_width,
            control_button_height,
            False,
            is_cancel_hovered
        )
        
        buttons.extend([("Apply and go back", apply_rect), ("Cancel and go back", cancel_rect)])
        return buttons

    def draw_about_menu(self):
        # Load and draw the new background
        pathutil = PathUtils()
        about_bg_path = pathutil.get_image_path('about_us_background.png')
        about_background = pg.image.load(about_bg_path)
        about_background = pg.transform.scale(about_background, (self.width, self.height))
        self.surface.blit(about_background, (0, 0))

        # Title with outline
        title_font = self.font_manager.get_submenu_font(int(self.height / 3))  # Changed from /4 to /3 for larger font
        self.ui.draw_text_with_outline(
            self.surface,
            "About Us",
            title_font,
            (255, 255, 255),
            self.width // 2,
            100,  # Moved down from 80 to 100
            outline_width=3
        )

        # Team members data
        team_members = [
            {
                "name": "Mojtaba Malek-Nejad",
                "intro": "Game Developer | Loves creating games.",
                "email": "mojtaba.malek-nejad@uni-konstanz.de",
                "gitlab": "gitlab.inf.uni-konstanz.de/mojtaba.malek-nejad",
                "img": "Moj.jpg"
            },
            {
                "name": "Max Weber",
                "intro": "Frontend Developer and UI/UX Designer | Passionate about interactive visuals.",
                "email": "max.weber@uni.kn",
                "gitlab": "gitlab.inf.uni-konstanz.de/max.weber",
                "img": "MaxWeber.jpg"
            },
            {
                "name": "Philipp Gelfuss",
                "intro": "Backend Engineer | Makes everything run smoothly.",
                "email": "philipp.gelfuss@uni-konstanz.de",
                "gitlab": "gitlab.inf.uni-konstanz.de/philipp.gelfuss",
                "img": "philipp.png"
            }
        ]

        # Button dimensions and positioning
        button_font = self.font_manager.get_button_font(self.height // 20)
        button_x = 40  # Standard left margin
        button_width = self.width - (2 * button_x)  # Full width minus margins plus 60 pixels (increased from 20)
        button_height = 120  # Restored from 100 to original 120
        button_spacing = 15  # Reduced from 20 to 15 for tighter spacing
        start_y = 140  # Moved up from 150 to 140 to be closer to title

        # First pass: Load original images and find the most portrait-oriented one
        max_aspect_ratio = 1.0  # Default to square aspect ratio
        original_images = {}
        pathutil = PathUtils()

        # First load all images and check if they're valid
        valid_images_exist = False
        for member in team_members:
            if member["img"] not in self.team_images_cache:
                try:
                    img_path = pathutil.get_image_path(member["img"])
                    original_img = pg.image.load(img_path)
                    if original_img and original_img.get_width() > 0:  # Verify image is valid
                        original_images[member["img"]] = original_img
                        # Calculate aspect ratio (height/width)
                        aspect_ratio = original_img.get_height() / original_img.get_width()
                        max_aspect_ratio = max(max_aspect_ratio, aspect_ratio)
                        valid_images_exist = True
                except Exception as e:
                    print(f"Could not load image {member['img']}: {e}")
                    original_images[member["img"]] = None

        # Calculate the target width based on the most portrait-oriented image
        if valid_images_exist:
            vertical_padding = 7  # Maintain the same vertical padding
            available_height = button_height - (2 * vertical_padding)  # Height available for image
            target_width = int(available_height / max_aspect_ratio)  # Use the most portrait-oriented aspect ratio
        else:
            target_width = button_height  # Default to full height if no valid images

        text_offset = target_width + 40  # Space for image plus padding

        # Second pass: Scale all images to the target width while maintaining their original aspect ratios
        for img_name, original_img in original_images.items():
            if original_img is not None:
                try:
                    # Calculate height maintaining original aspect ratio
                    aspect_ratio = original_img.get_height() / original_img.get_width()
                    target_height = int(target_width * aspect_ratio)
                    
                    # Scale image
                    scaled_img = pg.transform.scale(original_img, (target_width, target_height))
                    # Apply rounded corners with the same radius as buttons
                    rounded_img = self.apply_rounded_corners(scaled_img, 10)  # Using same radius as buttons
                    self.team_images_cache[img_name] = rounded_img
                except Exception as e:
                    print(f"Could not scale image {img_name}: {e}")
                    self.team_images_cache[img_name] = None

        buttons = []
        mouse_pos = pg.mouse.get_pos()

        # Create large buttons for each team member
        for i, member in enumerate(team_members):
            y_pos = start_y + (i * (button_height + button_spacing))
            
            # Create button rect for collision detection
            button_rect = pg.Rect(button_x, y_pos, button_width, button_height)
            is_hovered = button_rect.collidepoint(mouse_pos)

            # Draw the large stone button
            rect = self.ui.draw_stone_button(
                self.surface,
                "",  # Empty text as we'll draw content manually
                button_font,
                button_x,
                y_pos,
                button_width,
                button_height,
                False,
                is_hovered,
                is_about_button=True  # Use high-quality texture for About Us buttons
            )

            # Draw the member's image if available
            if member["img"] in self.team_images_cache and self.team_images_cache[member["img"]] is not None:
                img = self.team_images_cache[member["img"]]
                # Add constant vertical padding (7px) regardless of image height
                vertical_padding = 7
                # Center image vertically in button with added padding
                available_height = button_height - (2 * vertical_padding)
                img_y = y_pos + vertical_padding + (available_height - img.get_height()) // 2
                self.surface.blit(img, (button_x + 10, img_y))  # 10px padding from button edge

            # Draw member information on the button
            name_font = pg.font.SysFont("Arial", 22, bold=True)
            role_font = pg.font.SysFont("Arial", 18)
            contact_font = pg.font.SysFont("Arial", 14)

            # Calculate text positions - now offset by image width
            text_x = button_x + text_offset  # Offset text by image width plus padding
            name_y = y_pos + 20
            role_y = name_y + 25
            email_y = role_y + 25

            # Draw shadow texts
            name_shadow = name_font.render(member["name"], True, (30, 30, 30))
            role_shadow = role_font.render(member["intro"], True, (30, 30, 30))
            email_shadow = contact_font.render(f"Email: {member['email']}", True, (30, 30, 30))

            # Draw main texts
            name_surface = name_font.render(member["name"], True, (255, 255, 255))
            role_surface = role_font.render(member["intro"], True, (170, 255, 170))
            email_surface = contact_font.render(f"Email: {member['email']}", True, (170, 170, 255))

            # Draw shadows
            shadow_offset = 2
            self.surface.blit(name_shadow, (text_x + shadow_offset, name_y + shadow_offset))
            self.surface.blit(role_shadow, (text_x + shadow_offset, role_y + shadow_offset))
            self.surface.blit(email_shadow, (text_x + shadow_offset, email_y + shadow_offset))

            # Draw texts
            self.surface.blit(name_surface, (text_x, name_y))
            self.surface.blit(role_surface, (text_x, role_y))
            self.surface.blit(email_surface, (text_x, email_y))

            # Store button with member data for click handling
            buttons.append(("dev_button", rect, member["email"]))

        # Add small back button with standard menu button dimensions
        button_texts = ["Back"]
        button_font = self.font_manager.get_button_font(self.height // 1)  # Größere Font-Größe
        back_button_width = self.ui.get_max_button_width(button_texts, button_font)
        button_height = button_font.get_height() + 15
        
        # Position for back button
        back_x = 40
        back_y = self.height - button_height - 15  # Changed from 40 to 30 to move button lower
        
        # Check for hover state
        mouse_pos = pg.mouse.get_pos()
        back_rect_bounds = pg.Rect(back_x, back_y, back_button_width, button_height)
        is_back_hovered = back_rect_bounds.collidepoint(mouse_pos)
        
        # Draw back button with standard style
        back_rect = self.ui.draw_stone_button(
            self.surface,
            "Back",
            button_font,
            back_x,
            back_y,
            back_button_width,
            button_height,
            False,
            is_back_hovered,
            is_about_button=True
        )
        
        buttons.append(("Back", back_rect, None))

        return buttons

    def handle_menu_click(self, pos, buttons):
        for button_data in buttons:
            if len(button_data) == 2:  # Old format (text, rect)
                text, rect = button_data
                email = None
            else:  # New format (text, rect, email)
                text, rect, email = button_data

            if rect.collidepoint(pos):
                current_menu = self.state.get_current_menu()
                
                # Handle Demo button click
                if text == "DEMO":
                    self.demo_selected = not self.demo_selected  # Toggle selected state
                    return "continue"
                
                if current_menu == self.state.MAIN:
                    if text == "Start Game (Enter)":
                        return "start_game"
                    elif text == "Change Mode":
                        self.state.switch_to_mode()
                    elif text == "Change Difficulty":
                        self.state.switch_to_difficulty()
                    elif text == "About Us":
                        self.state.switch_to_about()
                    elif text == "Quit Game":
                        return "quit_game"
                
                elif current_menu == self.state.MODE:
                    if text in self.state.modes:
                        self.state.select_mode(text)
                    elif text == "Apply and go back":
                        self.state.apply_mode()
                    elif text == "Cancel and go back":
                        self.state.cancel_selection()
                
                elif current_menu == self.state.DIFFICULTY:
                    if text in self.state.difficulties:
                        self.state.select_difficulty(text)
                    elif text == "Apply and go back":
                        self.state.apply_difficulty()
                    elif text == "Cancel and go back":
                        self.state.cancel_selection()
                
                elif current_menu == self.state.ABOUT:
                    if text == "Back":
                        self.state.switch_to_main()
                    elif text == "dev_button" and email:
                        # Open default email client with developer's email
                        import webbrowser
                        webbrowser.open(f'mailto:{email}')
                
                return "continue"
        return "continue"

    def draw_current_menu(self):
        if self.state.current_menu == self.state.MAIN:
            return self.draw_main_menu()
        elif self.state.current_menu == self.state.MODE:
            return self.draw_mode_menu()
        elif self.state.current_menu == self.state.DIFFICULTY:
            return self.draw_difficulty_menu()
        elif self.state.current_menu == self.state.ABOUT:
            return self.draw_about_menu()
        return []

    def get_selected_mode(self):
        return self.state.get_selected_mode()

    def get_selected_difficulty(self):
        return self.state.get_selected_difficulty()
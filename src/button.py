import pygame

class Button:
    def __init__(self, x, y, width, height, text, font, idle_color, hover_color, text_color, state="normal"):
        """
        x, y: Button position
        width, height: Button size
        text: Text displayed on the button
        font: Font used for the text
        idle_color: Button color when not hovered
        hover_color: Button color when hovered
        text_color: Text color
        state: Button state, either 'normal' or 'disabled'. Default is 'normal'
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.idle_color = idle_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.state = state  # New state parameter (default is "normal")

    def draw(self, surface):
        # If the button is disabled, set the color to a grayish tone
        if self.state == "disabled":
            color = (169, 169, 169)  # Disabled color (gray)
        else:
            mouse_pos = pygame.mouse.get_pos()
            # Change color when hovered, only if button is not disabled
            color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.idle_color
        
        # Draw the button
        pygame.draw.rect(surface, color, self.rect, border_radius=10)

        # Render and draw the text
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, event):
        # If the button is disabled, don't allow any clicks
        if self.state == "disabled":
            return False

        # Check if the button was clicked
        return (
            event.type == pygame.MOUSEBUTTONDOWN and
            event.button == 1 and
            self.rect.collidepoint(event.pos)
        )

    def set_state(self, state):
        """Method to change the state of the button."""
        self.state = state

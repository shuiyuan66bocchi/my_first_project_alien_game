import pygame
from pygame.sprite import Sprite


class Shield(Sprite):
    """A class to manage the ship's shield."""

    def __init__(self, ai_game):
        """Initialize the shield."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.ship = ai_game.ship
        
        # Shield properties
        self.active = False
        self.time_remaining = 0
        self.cooldown = 0
        
        # Shield settings
        self.duration = 5  # seconds
        self.cooldown_duration = 10  # seconds
        self.max_charges = 3
        self.charges = self.max_charges
        
        # Visual properties
        self.color = (0, 191, 255)  # Light blue
        self.width = 3
        self.radius_increase = 15
        
        # Create shield surface for transparency
        self.create_shield_surface()

    def create_shield_surface(self):
        """Create a surface for the shield with transparency."""
        max_size = max(self.ship.rect.width, self.ship.rect.height) + self.radius_increase * 2
        self.surface = pygame.Surface((max_size, max_size), pygame.SRCALPHA)
        self.rect = self.surface.get_rect()

    def activate(self):
        """Activate the shield if available."""
        if not self.active and self.cooldown <= 0 and self.charges > 0:
            self.active = True
            self.time_remaining = self.duration
            self.charges -= 1
            return True
        return False

    def update(self):
        """Update shield timer and cooldown."""
        # Update active shield timer
        if self.active:
            self.time_remaining -= 1/60  # 60 FPS
            if self.time_remaining <= 0:
                self.active = False
                self.cooldown = self.cooldown_duration
        
        # Update cooldown
        if self.cooldown > 0:
            self.cooldown -= 1/60  # 60 FPS
            
            # Recharge when cooldown finishes
            if self.cooldown <= 0 and self.charges < self.max_charges:
                self.charges += 1
                # Start new cooldown if not at max charges
                if self.charges < self.max_charges:
                    self.cooldown = self.cooldown_duration

    def draw(self):
        """Draw the shield if active."""
        if self.active:
            # Update shield position to follow ship
            self.rect.center = self.ship.rect.center
            
            # Clear the surface
            self.surface.fill((0, 0, 0, 0))
            
            # Draw pulsating effect
            pulse = abs(pygame.time.get_ticks() % 1000 - 500) / 500  # 0 to 1 back to 0
            current_width = int(self.width + pulse * 2)
            current_radius = self.radius_increase + int(pulse * 5)
            
            # Draw outer shield circle
            pygame.draw.circle(
                self.surface, 
                self.color, 
                (self.rect.width // 2, self.rect.height // 2),
                max(self.ship.rect.width, self.ship.rect.height) // 2 + current_radius,
                current_width
            )
            
            # Draw inner shield circle
            inner_color = (min(255, self.color[0] + 50), 
                          min(255, self.color[1] + 50), 
                          min(255, self.color[2] + 50), 
                          100)
            pygame.draw.circle(
                self.surface,
                inner_color,
                (self.rect.width // 2, self.rect.height // 2),
                max(self.ship.rect.width, self.ship.rect.height) // 2 + current_radius - 5,
                1
            )
            
            # Blit the shield surface to the screen
            self.screen.blit(self.surface, self.rect)

    def get_status_text(self):
        """Get text describing current shield status."""
        if self.active:
            return f"SHIELD: {self.time_remaining:.1f}s"
        elif self.charges > 0:
            if self.cooldown > 0:
                return f"SHIELD: {self.charges} (CD: {self.cooldown:.1f}s)"
            else:
                return f"SHIELD: {self.charges} (Press 1)"
        else:
            return f"SHIELD: 0 (CD: {self.cooldown:.1f}s)"

    def get_status_color(self):
        """Get color for status text based on shield state."""
        if self.active:
            return (0, 191, 255)  # Blue when active
        elif self.charges > 0:
            if self.cooldown > 0:
                return (255, 165, 0)  # Orange when charging
            else:
                return (0, 255, 0)    # Green when ready
        else:
            return (255, 0, 0)        # Red when unavailable

    def reset(self):
        """Reset shield to initial state."""
        self.active = False
        self.time_remaining = 0
        self.cooldown = 0
        self.charges = self.max_charges
import pygame
import ctypes
import math

# Load the shared library
libpendulum = ctypes.CDLL('./libpendulum.so')

# Define the updatePendulum function signature
libpendulum.updatePendulum.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_double, ctypes.c_double, ctypes.c_double]

# Constants
PI = 3.141592653589793
length = 100.0
initialPivotX = 400.0
initialPivotY = 200.0
pivotRadius = 10.0
maxHorizontalDisplacement = 100.0

def main():
    # Initialize Pygame
    pygame.init()
    window = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Water Sloshing Simulation")

    # Pendulum properties
    angle = ctypes.c_double(PI * 2)
    angular_velocity = ctypes.c_double(0.0)  

    # Pendulum Red Ball
    bob_radius = 10
    bob_color = (255, 0, 0)

    # Pendulum Blue Ball
    pivot_color = (0, 0, 255)
    pivot_position = pygame.Vector2(initialPivotX, initialPivotY)

    # Pendulum rod
    line_color = (255, 255, 255)

    is_dragging = False
    drag_offset = pygame.Vector2(0, 0)

    prev_pivot_x = initialPivotX
    prev2_pivot_x = initialPivotX

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if pygame.Rect(pivot_position.x - pivotRadius, pivot_position.y - pivotRadius, 2 * pivotRadius, 2 * pivotRadius).collidepoint(mouse_pos):
                        is_dragging = True
                        drag_offset = pivot_position - pygame.Vector2(mouse_pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    is_dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if is_dragging:
                    mouse_pos = pygame.mouse.get_pos()
                    new_x = mouse_pos[0] + drag_offset.x

                    # Move units left and right
                    if new_x < initialPivotX - maxHorizontalDisplacement:
                        new_x = initialPivotX - maxHorizontalDisplacement
                    if new_x > initialPivotX + maxHorizontalDisplacement:
                        new_x = initialPivotX + maxHorizontalDisplacement

                    pivot_position.x = new_x

        # Update the pendulum
        current_pivot_x = pivot_position.x
        libpendulum.updatePendulum(ctypes.byref(angle), ctypes.byref(angular_velocity), current_pivot_x, prev_pivot_x, prev2_pivot_x)
        prev2_pivot_x = prev_pivot_x
        prev_pivot_x = current_pivot_x

        # Calculate bob position
        x = pivot_position.x + length * math.sin(angle.value)
        y = pivot_position.y + length * math.cos(angle.value)
        bob_position = pygame.Vector2(x, y)

        # Clear the window
        window.fill((0, 0, 0))

        # Draw the rod
        pygame.draw.line(window, line_color, pivot_position, bob_position, 2)

        # Draw the pivot
        pygame.draw.circle(window, pivot_color, (int(pivot_position.x), int(pivot_position.y)), pivotRadius)

        # Draw the bob
        pygame.draw.circle(window, bob_color, (int(bob_position.x), int(bob_position.y)), bob_radius)

        # Update the display
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()


# To run: python3 Sloshing_Simulation.py





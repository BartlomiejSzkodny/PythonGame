import pygame


class Entity(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.status = 'down'
        self.frame_index = 0
        self.animation_speed = 7
        self.damage = 0
        self.direction = pygame.math.Vector2()

    def collision(self, direction):
        for sprite in self.collision_sprites.sprites():
            if sprite.hitbox.colliderect(self.hitbox):
                if direction == "horizontal":
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                    self.rect.centerx = self.hitbox.centerx
                    self.pos.x = self.rect.centerx
                if direction == "vertical":
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                    self.rect.centery = self.hitbox.centery
                    self.pos.y = self.rect.centery

    def move(self, dt):
        if self.direction.length() > 0:
            self.direction.normalize_ip()

        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision('horizontal')

        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision('vertical')

    def update(self, dt):
        self.image = self.animations[self.status][self.frame_index]
        self.move(dt)
        self.animate()

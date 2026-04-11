def resolve(rect, vel_x, vel_y, rotation, platforms, dt):
    """
    Move rect by velocity, resolve collisions against platforms, return
    (vel_x, vel_y, on_ground). rect is mutated in place.
    """
    on_ground = False

    # ── X axis ──
    rect.x += vel_x * dt
    for plat in platforms:
        if not rect.colliderect(plat):
            continue
        overlap = min(rect.right, plat.right) - max(rect.left, plat.left)
        if rect.centerx < plat.centerx:
            rect.x -= overlap
            if rotation == 90:
                on_ground = True
        else:
            rect.x += overlap
            if rotation == 270:
                on_ground = True
        vel_x = 0.0

    # ── Y axis ──
    rect.y += vel_y * dt
    for plat in platforms:
        if not rect.colliderect(plat):
            continue
        overlap = min(rect.bottom, plat.bottom) - max(rect.top, plat.top)
        if rect.centery < plat.centery:
            rect.y -= overlap
            if rotation == 0:
                on_ground = True
        else:
            rect.y += overlap
            if rotation == 180:
                on_ground = True
        vel_y = 0.0

    return vel_x, vel_y, on_ground

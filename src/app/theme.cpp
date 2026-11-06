// ProsperoRadio - Night Signal: the app's design language as kit tokens.
// Petunia: Nightshade's black, with chartreuse for its red.
// Copyright (C) 2026 BlackBearReloaded
// SPDX-License-Identifier: GPL-3.0-or-later

#include "app/theme.hpp"

namespace radio
{

ui::Theme night_signal()
{
    // The kit's Acrylic theme is the recipe (glass surfaces, hairlines of
    // light); the palette and the corners are Nightshade's, with Petunia's
    // chartreuse for its red; the pace is ProsperoRadio's own.
    ui::Theme t = ui::themes()[0];
    t.id = APP_DATA_NAME;
    t.name = APP_TITLE_NAME;
    t.family = "Frosted glass";
    t.summary = "Black glass over a near-black sky with a low chartreuse glow";

    t.backdrop = night_sky(tone::accent, tone::olive, 0.0f, 0.0f);
    t.page = tone::night;
    t.surface = tone::panel.with_alpha(0.5f);
    t.surface_high = Color::rgb(0xffffff, 0.1f);
    t.text = Color::rgb(0xededf0);
    t.text_muted = Color::rgb(0xededf0, 0.62f);
    t.primary = tone::accent;
    t.on_primary = tone::ink;
    t.secondary = Color::rgb(0xffffff, 0.08f);
    t.on_secondary = Color::rgb(0xededf0);
    t.accent = tone::accent;
    t.outline = Color::rgb(0xffffff, 0.12f);
    t.focus = tone::accent;
    t.shadow = Color::rgb(0x000000, 0.45f);
    t.light = Color::rgb(0xffffff, 0.22f);
    t.danger = Color::rgb(0xff7a7a);
    t.success = tone::good;
    t.warning = Color::rgb(0xf0a35e); // amber, never the accent

    t.style = ui::SurfaceStyle::glass;
    t.corner = ui::Corner::round;
    t.radius = 12.0f;
    t.radius_card = 20.0f;
    t.border = 1.5f;
    t.pill_chips = true;
    t.shadow_offset = 12.0f;
    t.shadow_blur = 32.0f;
    t.focus_width = 3.0f;
    t.focus_gap = 5.0f;

    t.heading = ui::FontRole::display;
    t.label = ui::FontRole::semibold;
    t.omega = 18.0f;
    t.damping = 1.0f;
    t.sounds = audio::SoundSet::glass;
    t.dark = true;
    return t;
}

gfx::BackdropSpec night_sky(Color lean, Color lean_dark, float amount, float time)
{
    gfx::BackdropSpec sky;
    sky.mode = gfx::BackdropMode::aurora;
    sky.colors[0] = Color::rgb(0x0e0e11);
    sky.colors[1] = Color::rgb(0x050506);
    // The clouds stay dark: they are a mood behind text, not a picture. Both
    // are Petunia's chartreuse, as low as Nightshade's red glow: a dim olive
    // and the deep olive under it.
    sky.colors[2] = gfx::mix(Color::rgb(0x3f5808), gfx::mix(lean, tone::night, 0.45f), amount);
    sky.colors[3] = gfx::mix(Color::rgb(0x222f06), gfx::mix(lean_dark, lean, 0.25f), amount);
    sky.time = time;
    return sky;
}

} // namespace radio

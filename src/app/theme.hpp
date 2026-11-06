// ProsperoRadio - Night Signal: the app's design language as kit tokens.
// Petunia: Nightshade's black, with chartreuse for its red.
// Copyright (C) 2026 BlackBearReloaded
// SPDX-License-Identifier: GPL-3.0-or-later

#pragma once

#include "app/kit.hpp"

namespace radio
{

// Colours that mean something in this app and are not part of a ui::Theme.
// Petunia: Nightshade's palette (its "nightly" theme, as Physalis and Datura have it), near
// black and clean, with Petunia's chartreuse where the family has its red. Text on the accent
// is always ink: ink on it reads at 13.6:1, white at 1.4:1.
namespace tone
{
inline const Color accent = Color::rgb(0xaeea00);  // chartreuse: the brand accent (13.8:1 on night)
inline const Color olive = Color::rgb(0x2a3a08);   // deep olive: the dark half of its light
inline const Color live = Color::rgb(0xff6b72);    // "on air": the family's red, as a studio light
inline const Color gold = Color::rgb(0xffd166);    // a favourite
inline const Color ink = Color::rgb(0x0b0b0d);     // text and icons on the accent or a white button
inline const Color night = Color::rgb(0x09090b);   // the page behind everything
inline const Color panel = Color::rgb(0x0e0e11);   // panels and tiles
inline const Color row_lit = Color::rgb(0x1a2110); // a row or tile in focus
inline const Color good = Color::rgb(0x6fe3ae);    // done, saved
} // namespace tone

// Black glass over a near-black sky with a low chartreuse glow, chartreuse as the one accent.
ui::Theme night_signal();

// The aurora behind the screens, with its two clouds leaning toward `lean`
// (the colour of the station in focus) by `amount` (0..1).
gfx::BackdropSpec night_sky(Color lean, Color lean_dark, float amount, float time);

} // namespace radio

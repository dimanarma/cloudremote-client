#!/usr/bin/env python3
"""CloudRemote branding: bake server address, key and app name into hbb_common.
Runs in CI after `submodules: recursive` checkout, so it patches the freshly
fetched upstream libs/hbb_common/src/config.rs. Idempotent and fails loudly if
an expected anchor is missing (so an upstream change can't silently un-brand)."""
import sys

CFG = "libs/hbb_common/src/config.rs"

SERVER = "185.143.177.51"
PUBKEY = "0JebK4pT40g8kZOMivtBLgRfKVsDMFNOP6dWDhIq4V0="
APP_NAME = "CloudRemote"

REPLACEMENTS = [
    (
        'pub static ref APP_NAME: RwLock<String> = RwLock::new("RustDesk".to_owned());',
        f'pub static ref APP_NAME: RwLock<String> = RwLock::new("{APP_NAME}".to_owned());',
    ),
    (
        'pub const RENDEZVOUS_SERVERS: &[&str] = &["rs-ny.rustdesk.com"];',
        f'pub const RENDEZVOUS_SERVERS: &[&str] = &["{SERVER}"];',
    ),
    (
        'pub const RS_PUB_KEY: &str = "OeVuKk5nlHiXp+APNn0Y3pC1Iwpwn44JGqrQCsWqmBw=";',
        f'pub const RS_PUB_KEY: &str = "{PUBKEY}";',
    ),
]

with open(CFG, "r", encoding="utf-8") as f:
    src = f.read()

for old, new in REPLACEMENTS:
    if new in src:
        continue  # already branded (idempotent)
    if old not in src:
        sys.exit(f"[cloudremote_brand] anchor not found, cannot brand: {old!r}")
    src = src.replace(old, new)

with open(CFG, "w", encoding="utf-8") as f:
    f.write(src)

print(f"[cloudremote_brand] server={SERVER} app={APP_NAME} key set OK")

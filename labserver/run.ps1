# Cybersecurity-Mastery - an interactive, offline cybersecurity learning app.
# Copyright (C) 2026 Nithees Narendra S
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This file is part of Cybersecurity-Mastery. It is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version. There is NO WARRANTY. See the
# LICENSE file for the full text. For use outside the GPL-3.0 terms (e.g.
# proprietary/commercial), contact the copyright holder for a separate licence.

# Cybersecurity-Mastery — Lab Runner (Windows)
# Runs the local execution backend so the site's "Run" buttons work.
$ErrorActionPreference = "Stop"
Set-Location -Path $PSScriptRoot
python server.py

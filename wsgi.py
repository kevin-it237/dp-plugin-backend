# Copyright (c) 2024 Abel Kevin Ngaleu, University of Luxembourg
# This software is licensed under the MIT License.
# See the LICENSE file for more details.

from dp_plugin import create_app

app = create_app()

if __name__ == "__main__":
        app.run(host="0.0.0.0")
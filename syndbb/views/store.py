#
# Copyright (c) 2017 by faggqt (https://faggqt.pw). All Rights Reserved.
# You may use, distribute and modify this code under the QPL-1.0 license.
# The full license is included in LICENSE.md, which is distributed as part of this project.
#

import syndbb

# Pages
@syndbb.app.route("/store/")
def store():
    return syndbb.render_template('store.html', title="Store", subheading=[""])

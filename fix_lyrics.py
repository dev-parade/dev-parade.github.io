import re

with open('/Users/coyass/kaihatsu/dev-parade-site/lyrics/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Pattern to find:
#         <!-- AI Insight -->
#         <div class="ai-insight">
#           ...
#         </div>
#       </div>  (this is the lyrics-body's closing div in the previous structure, wait)
# 
# Actually, the AI Insight is currently INSIDE lyrics-body for some, and OUTSIDE for others.
# Let's see how we can move ALL of them to just OUTSIDE lyrics-body.


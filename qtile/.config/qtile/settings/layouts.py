from libqtile import layout
from libqtile.config import Match



#DISEÑOS DE VENTANAS / LAYOUTS
layouts = [
    layout.Columns(border_focus="#e3dac9", border_width=2, margin=3),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(border_focus="#e3dac9", border_width=2, margin=6),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="Helvetica", # change to helvetica # # Antes font="Hack Regular" #
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()
package com.robisa693.musiccapehelper;

import net.runelite.client.config.Config;
import net.runelite.client.config.ConfigGroup;
import net.runelite.client.config.ConfigItem;
import net.runelite.client.config.ConfigSection;

@ConfigGroup("musiccapehelper")
public interface MusicCapeHelperConfig extends Config
{
    enum ClickMode
    {
        WIKI,
        MAP
    }

    @ConfigSection(
        name = "Display",
        description = "Display options",
        position = 0
    )
    String displaySection = "display";

    @ConfigItem(
        keyName = "showMissingOnly",
        name = "Show missing only",
        description = "Only show tracks that are still locked",
        position = 1,
        section = displaySection
    )
    default boolean showMissingOnly()
    {
        return false;
    }

    @ConfigItem(
        keyName = "groupByArea",
        name = "Group by area",
        description = "Group tracks by area instead of showing a flat list",
        position = 2,
        section = displaySection
    )
    default boolean groupByArea()
    {
        return true;
    }

    @ConfigSection(
        name = "Click Behaviour",
        description = "What happens when you click a track",
        position = 10
    )
    String clickSection = "click";

    @ConfigItem(
        keyName = "clickMode",
        name = "Click mode",
        description = "Wiki: open OSRS Wiki page. Map: open in-game world map at the track's location.",
        position = 11,
        section = clickSection
    )
    default ClickMode clickMode()
    {
        return ClickMode.WIKI;
    }
}

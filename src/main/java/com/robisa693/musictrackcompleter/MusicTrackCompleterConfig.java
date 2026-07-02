package com.robisa693.musictrackcompleter;

import net.runelite.client.config.Config;
import net.runelite.client.config.ConfigGroup;
import net.runelite.client.config.ConfigItem;

@ConfigGroup("musictrackcompleter")
public interface MusicTrackCompleterConfig extends Config
{
    @ConfigItem(
        keyName = "showMissingOnly",
        name = "Show missing only",
        description = "Only show tracks that are still locked",
        position = 1
    )
    default boolean showMissingOnly()
    {
        return false;
    }

    @ConfigItem(
        keyName = "groupByArea",
        name = "Group by area",
        description = "Group tracks by area instead of showing a flat list",
        position = 2
    )
    default boolean groupByArea()
    {
        return true;
    }
}

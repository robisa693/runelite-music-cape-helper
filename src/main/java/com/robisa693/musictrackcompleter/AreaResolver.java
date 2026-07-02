package com.robisa693.musictrackcompleter;

import java.util.HashMap;
import java.util.Map;

class AreaResolver
{
    private static final Map<Integer, String> AREA_NAMES = new HashMap<>();

    static
    {
        AREA_NAMES.put(47, "Lumbridge / Draynor");
        AREA_NAMES.put(45, "Varrock");
        AREA_NAMES.put(46, "Falador / Asgarnia");
        AREA_NAMES.put(48, "Karamja / Crandor");
        AREA_NAMES.put(49, "Fremennik Isles / Rellekka");
        AREA_NAMES.put(50, "Ardougne / Kandarin");
        AREA_NAMES.put(51, "Desert / Al Kharid");
        AREA_NAMES.put(52, "Wilderness");
        AREA_NAMES.put(53, "Morytania");
        AREA_NAMES.put(54, "Tirannwn / Prifddinas");
        AREA_NAMES.put(55, "Kourend / Zeah");
        AREA_NAMES.put(56, "Kebos Lowlands");
        AREA_NAMES.put(57, "Varlamore");
        AREA_NAMES.put(58, "Fossil Island");
        AREA_NAMES.put(59, "Miscellania / Etceteria");
        AREA_NAMES.put(60, "Lunar Isle");
        AREA_NAMES.put(61, "Entrana / Corsair Cove");
        AREA_NAMES.put(62, "Trollheim / God Wars");
        AREA_NAMES.put(63, "Feldip Hills / Gnome");
        AREA_NAMES.put(64, "Digsite / Fossil Island");
        AREA_NAMES.put(65, "Piscatoris / Ape Atoll");
        AREA_NAMES.put(66, "Dorgesh-Kaan / Keldagrim");
        AREA_NAMES.put(67, "Mos Le'Harmless / Harmony");
        AREA_NAMES.put(68, "Miscellaneous / Events");
        AREA_NAMES.put(69, "Taverley / Burthorpe");
        AREA_NAMES.put(70, "Camdozaal / Ice Mountain");
        AREA_NAMES.put(71, "Dungeons");
        AREA_NAMES.put(72, "Minigames");
        AREA_NAMES.put(73, "Bosses");
        AREA_NAMES.put(74, "Raids");
        AREA_NAMES.put(75, "Quest areas");
        AREA_NAMES.put(76, "Tutorial Island");
        AREA_NAMES.put(77, "Holiday / Special");
    }

    static String getAreaName(int areaId)
    {
        return AREA_NAMES.getOrDefault(areaId, "Area " + areaId);
    }
}

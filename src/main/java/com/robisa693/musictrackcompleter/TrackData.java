package com.robisa693.musictrackcompleter;

class TrackData
{
    final int dbRow;
    final String displayName;
    final String unlockHint;
    final int areaId;
    final String sortName;
    final boolean hidden;

    TrackData(int dbRow, String displayName, String unlockHint, int areaId, boolean hidden)
    {
        this.dbRow = dbRow;
        this.displayName = displayName;
        this.unlockHint = unlockHint;
        this.areaId = areaId;
        this.hidden = hidden;
        this.sortName = displayName.replaceAll("^(A|An|The)\\s+", "");
    }
}

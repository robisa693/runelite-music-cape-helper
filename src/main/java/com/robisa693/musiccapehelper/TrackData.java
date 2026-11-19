package com.robisa693.musiccapehelper;

class TrackData
{
    final int dbRow;
    final String displayName;
    final String unlockHint;
    final int areaId;
    final boolean hidden;
    final boolean holiday;

    TrackData(int dbRow, String displayName, String unlockHint, int areaId, boolean hidden, boolean holiday)
    {
        this.dbRow = dbRow;
        this.displayName = displayName;
        this.unlockHint = unlockHint;
        this.areaId = areaId;
        this.hidden = hidden;
        this.holiday = holiday;
    }
}

# Debug cheatsheet

Some debug-releated one-liners for use in the python REPL. Everything should be ran from within the `whow` directory.

## Schedule Testing:
One Liner:
```py
import util; import datetime; dn=datetime.datetime.now(); util.build_schedule_tree(dn.time(), {"mon": util.ScheduleDay("mon", [util.ScheduleEntry(dn.time(), None, "arstarst", []), util.ScheduleEntry(dn.time(), None, "tarstars", [])], False), "thu": util.ScheduleDay("thu", [util.ScheduleEntry(dn.time(), None, "aouywfdharluyoths", [])], True)})
```

Expanded:
```py
import util
import datetime
dn = datetime.datetime.now()
util.build_schedule_tree(
    dn.time(),
    {
        "mon": util.ScheduleDay("mon", [
            util.ScheduleEntry(dn.time(), None, "arstarst", []),
            util.ScheduleEntry(dn.time(), None, "tarstars", [])
        ], False),
        "thu": util.ScheduleDay("thu", [
            util.ScheduleEntry(dn.time(), None, "aouywfdharluyoths", [])
        ], True)
    }
)
```

Expected Output:

something like `{'schedule': {'anchor_date': datetime.time(11, 18, 37, 800626), 'repeats': ['thu'], 'days': {'mon': [{'begin': datetime.time(11, 18, 37, 800626), 'end': '', 'label': 'arstarst', 'categories': []}, {'begin': datetime.time(11, 18, 37, 800626), 'end': '', 'label': 'tarstars', 'categories': []}], 'thu': [{'begin': datetime.time(11, 18, 37, 800626), 'end': '', 'label': 'aouywfdharluyoths', 'categories': []}]}}}`

Expanded form: 
```py
{
    'schedule': {
        'anchor_date': datetime.time(11, 18, 37, 800626),
        'repeats': ['thu'],
        'days': {
            'mon': [
                {
                    'begin': datetime.time(11, 18, 37, 800626),
                    'end': '',
                    'label': 'arstarst',
                    'categories': []
                },
                {
                    'begin': datetime.time(11, 18, 37, 800626),
                    'end': '',
                    'label': 'tarstars',
                    'categories': []
                }
            ],
            'thu': [
                {
                    'begin': datetime.time(11, 18, 37, 800626),
                    'end': '',
                    'label': 'aouywfdharluyoths',
                    'categories': []
                }
            ]
        }
    }
}
```

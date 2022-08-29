# Canvas Parent API
This is an async wrapper for the [Canvas API](https://canvas.instructure.com/doc/api/) from Instructure.  There are a few types of objects this will retrieve based on the assumption that you are a parent with students enrolled with Canvas.  

The types of objects that can be returned include:
 - Observees (Students)
 - Courses
 - Assignments

This module is provided for use with the Home Assistant custom integration [Canvas](https://github.com/schwartzpub/canvas_hassio) however it could be useful as a standalone module for your own projects as well.

## Installing
To install the module use:
```python
python3 -m pip install canvas-parent-api
```

### Usage
Example usage to get students, printing names:
```python
import asyncio
from canvas_parent_api import Canvas

base_url = "https://school.instructure.com"
api_token = "randomstringthatisntreallyatoken"

async def get_students():
	client = Canvas(f"{base_url}",f"{api_token}")
	return await client.observees()

students = asyncio.run(get_students())

for student in students:
	print(student.name)
```

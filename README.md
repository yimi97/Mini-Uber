## Requirement Coverage(100%):

* 1 - 4: User-friendly UI. Easy to find button to signup, login and logout. Implemented validation based on the auth provided by django.

After login, you can enter the dashboard with the function navbar on the left.

* 5 - 6: Click `vehicle info`

If not register as driver yet, the browser will redirect to the register form.
If register, then the user can view and edit their profile.

* 7: Click `Start a Ride`

Fill out the form and will create a new ride.

* 8 - 12: Click `Rides`

The default filter is `Non-complete` status.
The page will display all the rides related to the user, also the allowed kinds of operations is aligned with the requirements.

**Our design Rule**

**Specifically, sharer can only view the ride detail, not editing.**

**Owner can only edit the ride if there is no sharer joined at that time.**


* 13 - 14: Click `Join a Ride`

* 15 - 17: Click `Search Ride`

* 18 - 20: Click `Ride` + Select role as Driver


## Run Instruction
`cd docker-deploy`

`sudo docker-compose up`

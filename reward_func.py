def reward_function(params):
    import math
    
    DIRECTION_THRESHOLD = 10 
    STEERING_THRESHOLD = 12.5
    MIN_REWARD = -1.0
    MAX_REWARD = 1.0
    MAX_STEPS = 300

    # Read input parameters
    distance_from_center = params['distance_from_center']
    on_track = params['all_wheels_on_track']
    progress = params['progress']
    track_width = params['track_width']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']
    steering = abs(params['steering_angle'])
    steps = params['steps']


    # Centering
    reward = math.exp(-6 * distance_from_center)

    if not on_track:
        reward = MIN_REWARD
        return reward
    elif progress == 1:
        reward = MAX_REWARD
        return reward
    else: 
        reward = MAX_REWARD * progress
        
    # Reward for staying away from borders
    distance_from_border = 0.5 * track_width - distance_from_center
    if distance_from_border < 0.05:
        reward *= MIN_REWARD - distance_from_border

    # Steering
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]

    track_direction =  math.atan2(next_point[1] - prev_point[1], next_point[0] -
            prev_point[0])

    track_direction = math.degrees(track_direction)

    direction_diff = abs(track_direction - heading)

    if direction_diff > DIRECTION_THRESHOLD:
        reward *= direction_diff / 100

    if steering > STEERING_THRESHOLD:
        reward *= STEERING_THRESHOLD / abs(steering)

    if (steps % 100) == 0 and progress > (steps / MAX_STEPS):
        reward += MAX_REWARD * 2


    return float(reward)


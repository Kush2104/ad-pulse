from flask import request, jsonify, Blueprint
from app.enums.States import States
from app.services.campaign_service import create_campaign, update_campaign, get_campaign_by_id, get_all_campaigns, \
    update_campaign_state, get_campaign_by_state

campaign_blueprint = Blueprint('campaign', __name__)


@campaign_blueprint.route('/campaign', methods=['POST'])
def create_campaign_api():
    # Parse JSON data from request
    json_data = request.json

    # Call the function to create a new campaign
    created_campaign = create_campaign(json_data)

    return jsonify({'message': 'Campaign created successfully',
                    'campaign': created_campaign
                    }), 201


@campaign_blueprint.route('/campaign', methods=['PUT'])
def update_campaign_api():
    # Parse JSON data from request
    json_data = request.json

    # Update the campaign
    updated_campaign = update_campaign(json_data)

    if updated_campaign:
        return jsonify({
            'message': 'Campaign updated successfully',
            'campaign': updated_campaign
        }), 200
    else:
        return jsonify({'error': 'Campaign not found'}), 404


@campaign_blueprint.route('/campaign/campaignid/<campaign_id>', methods=['GET'])
def get_campaign_api(campaign_id):
    # Get the campaign
    campaign = get_campaign_by_id(campaign_id)

    if campaign:
        return campaign, 200
    else:
        return jsonify({'error': 'Campaign not found'}), 404


@campaign_blueprint.route('/campaign', methods=['GET'])
def get_all_campaigns_api():
    # Get all campaigns
    campaigns = get_all_campaigns()

    return campaigns, 200


@campaign_blueprint.route('/campaign', methods=['PATCH'])
def update_campaign_state_api():
    campaign_id = request.args.get('campaign_id')
    new_state = request.args.get('new_state')
    if new_state not in States.__members__:
        return jsonify({'error': 'Invalid state'}), 400
    if new_state == States.CREATED.value:
        return jsonify({'error': 'Invalid State Transition'}), 400
    return update_campaign_state(campaign_id, new_state)


@campaign_blueprint.route('/campaign/state/<state>', methods=['GET'])
def get_publisher_by_state_api(state):
    if state not in States.__members__:
        return jsonify({'error': 'Invalid state'}), 400
    publishers = get_campaign_by_state(state)
    return publishers, 200


def get_new_form(old_form:dict) -> dict:
    form = {}

    form['title'] = old_form['info']['title']
    form['sections'] = []

    items_iter = iter(old_form['items'])
    first_item = next(items_iter)

    new_section = {
        'sectionId': 'FIRST_SECTION',
        'title': 'FIRST_SECTION',
        'items': [{
            'itemId': first_item['itemId'],
            'type': first_item['questionItem']['question']['choiceQuestion']['type'],
            'text': first_item['title'],
            'required': first_item['questionItem']['question'].get('required', False),
            'description': first_item.get('description', None),
            'options': [
                {
                    'value': option['value'],
                    'goToSectionId': option['goToSectionId']
                }
                for option in first_item['questionItem']['question']['choiceQuestion']['options']
            ]
        },]
    }

    for item in items_iter:
        print('ITEM = ', item['itemId'])
        if 'pageBreakItem' in item:
            form['sections'].append(new_section)

            new_section = {
                'sectionId': item['itemId'],
                'title': item['title'],
                'items': []
            }
        elif 'textItem' in item:
            print('TEXT ITEM')
            new_section['items'].append({
                'itemId': item['itemId'],
                'type': 'textItem',
                'text': item['title'],
                'description': item['description'],
            })
        elif 'questionGroupItem' in item:
            print('GROUP')
            pass
        elif 'scaleQuestion' in item['questionItem']['question']:
            print('SCALE')
            pass
        elif 'textQuestion' in item['questionItem']['question']:
            print('TEXT QUESTION')
            new_section['items'].append({
                'itemId': item['itemId'],
                'type': 'textQuestion',
                'paragraph': item['questionItem']['question']['textQuestion'].get('paragraph', None),
                'text': item['title'],
                'description': item.get('description', None),
            })
        elif 'timeQuestion' in item['questionItem']['question']:
            print('TIME')
            new_section['items'].append({
                'itemId': item['itemId'],
                'type': 'timeQuestion',
                'text': item['title'],
                'required': item['questionItem']['question'].get('required', False),
                'description': item.get('description', None),
            })
        elif 'dateQuestion' in item['questionItem']['question']:
            print('DATE')
            new_section['items'].append({
                'itemId': item['itemId'],
                'type': 'dateQuestion',
                'text': item['title'],
                'required': item['questionItem']['question'].get('required', False),
                'description': item.get('description', None),
            })
        else:
            new_section['items'].append({
                'itemId': item['itemId'],
                'type': item['questionItem']['question']['choiceQuestion']['type'],
                'text': item['title'],
                'required': item['questionItem']['question'].get('required', False),
                'description': item.get('description', None),
                'options': [
                    {
                        'value': option['value'],
                        'goToSectionId': option.get('goToSectionId', None)
                    }
                    for option in item['questionItem']['question']['choiceQuestion']['options'] if 'value' in option
                ]
            })          
        
    return form

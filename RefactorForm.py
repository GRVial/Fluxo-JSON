class RefactorForm:
    
    @classmethod
    def get_new_form(cls, old_form:dict) -> dict:
        title = old_form['info'].get('title', None)
        if title is None:
            title = old_form['info'].get('documentTitle', None)

        return {
            'title': title,
            'sections': cls._get_sections(old_form, title)
        }

    @classmethod
    def _get_sections(cls, old_form, title):
        sections = []

        current_section = {
            'sectionId': 'FIRST_SECTION',
            'title': title,
        }
        current_section_items = []

        for item in old_form['items']:
            if 'pageBreakItem' in item:
                current_section['items'] = current_section_items
                sections.append(current_section)

                current_section = cls._new_section(item)
                current_section_items = []
                continue
            
            if 'textItem' in item:
                new_item = cls._text_item(item)
            elif 'questionItem' in item:
                new_item = cls._question_item(item)
            elif 'questionGroupItem' in item:
                pass
            
            if new_item is not None:
                current_section_items.append(new_item)

        current_section['items'] = current_section_items
        sections.append(current_section)

        return sections

    @classmethod
    def _text_item(cls, item) -> dict:
        return {
            'itemId': item['itemId'],
            'type': 'textItem',
            'text': item.get('title', None),
            'description': item['description'],
        }
    
    @classmethod
    def _question_item(cls, item) -> dict:
        item_id = item['itemId']
        question_text = item.get('title', None)
        description = item.get('description', None)

        question = item['questionItem']['question']
        if 'scaleQuestion' in question:
            return None
        elif 'textQuestion' in question:
            new_item = cls._text_question(question)
        elif 'timeQuestion' in question:
            new_item = cls._time_question(question)
        elif 'dateQuestion' in question:
            new_item = cls._date_question(question)
        elif 'choiceQuestion' in question:
            new_item = cls._choice_question(question)

        if 'image' in item['questionItem']:
            image = item['questionItem']['image']['contentUri']
            new_item['image'] = image
        
        new_item['itemId'] = item_id
        new_item['description'] = description
        new_item['text'] = question_text
        return new_item

    @classmethod
    def _choice_question(cls, question) -> dict:
        return {
            'type': question['choiceQuestion']['type'],
            'required': question.get('required', False),
            'options': [
                {
                    'value': option['value'],
                    'goToSectionId': option.get('goToSectionId', None)
                }
                for option in question['choiceQuestion']['options'] if 'value' in option
            ]
        }

    @classmethod
    def _date_question(cls, question) -> dict:
        return {
            'type': 'dateQuestion',
            'required': question.get('required', False),
        }

    @classmethod
    def _time_question(cls, question) -> dict:
        return {
            'type': 'timeQuestion',
            'required': question.get('required', False),
        }

    @classmethod
    def _text_question(cls, question) -> dict:
        return {
            'type': 'textQuestion',
            'paragraph': question['textQuestion'].get('paragraph', None),
        }

    @classmethod
    def _new_section(cls, item) -> dict:
        new_section = {
                    'sectionId': item['itemId'],
                    'title': item.get('title', None),
                    'description': item.get('description', None)
                }
        
        return new_section

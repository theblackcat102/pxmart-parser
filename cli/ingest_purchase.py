from tqdm import tqdm
from modules.models import Purchase, px_db
from modules.parse_context import parse_html
from modules.list_mail import find_emails


if __name__ == '__main__':
    for (context, mail_html) in tqdm(find_emails()):
        if Purchase.select().where(Purchase.date == context['date']).exists():
            print('skipping {}'.format(context['date']))
            break
    
        items = parse_html(mail_html)
        for item in items:
            with px_db.atomic():
                Purchase.create(
                    name=item['name'],
                    count=item['count'],
                    total_price=item['price'],
                    date=context['date']
                )

        
        
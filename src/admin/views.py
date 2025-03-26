from sqladmin import ModelView

from db.models import Message, User, DepositVariant, \
	Payment, Setting, History, DayHint


class UserAdmin(ModelView, model=User):
	name = 'User'
	name_plural = 'Users'
	icon = 'fa-solid fa-user-group'
	page_size_options = [50, 100]

	column_list = [User.id, User.username, User.name, User.created_at]
	column_labels = {
		User.id: 'ID',
		User.created_at: 'Created at'
	}
	column_searchable_list = [User.id, User.username]
	form_excluded_columns = [User.created_at, User.updated_at]


class MessageAdmin(ModelView, model=Message):
	name = 'Message'
	name_plural = 'Messages'
	icon = 'fa-solid fa-font'

	column_list = [Message.id, Message.key, Message.value, Message.description]
	column_labels = {
		Message.id: 'ID',
		Message.key: 'Sys. Name',
	}


class DepositVariantAdmin(ModelView, model=DepositVariant):
	name = 'Deposit Variant'
	name_plural = 'Deposit Variants'
	icon = 'fa-solid fa-hand-holding-dollar'

	column_list = [DepositVariant.id, DepositVariant.count, DepositVariant.price]
	column_labels = {
		DepositVariant.id: 'ID',
		DepositVariant.count: 'Day Count',
	}


class PaymentAdmin(ModelView, model=Payment):
	name = 'Payment'
	name_plural = 'Payments'
	icon = 'fa-solid fa-money-bills'

	column_list = [Payment.id, Payment.tg_id, Payment.amount, Payment.count]
	column_labels = {
		Payment.id: 'ID',
		Payment.tg_id: 'TG ID',
		Payment.amount: 'Price',
		Payment.count: 'Day Count',
	}

	form_excluded_columns = [History.created_at, History.updated_at]


class SettingAdmin(ModelView, model=Setting):
	name = 'Setting'
	name_plural = 'Setting'
	icon = 'fa-solid fa-gear'

	column_list = [Setting.id, Setting.key, Setting.value, Setting.description]
	column_labels = {
		Setting.id: 'ID',
		Setting.key: 'Sys. Name',
	}


class HistoryAdmin(ModelView, model=History):
	name = 'History'
	name_plural = 'History'
	icon = 'fa-solid fa-address-book'

	column_list = [History.id, History.tg_id, History.role, History.content]
	column_labels = {
		History.id: 'ID',
		History.tg_id: 'TG ID',
	}

	form_excluded_columns = [History.created_at, History.updated_at]


class DayHintAdmin(ModelView, model=DayHint):
	name = 'Hint'
	name_plural = 'Hints'
	icon = 'fa-solid fa-book'

	column_list = [DayHint.id, DayHint.hint]
	column_labels = {
		History.id: 'ID',
	}

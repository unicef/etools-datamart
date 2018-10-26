UPDATE auth_user
SET
  password   = '',
  email      = CONCAT('username', id, '@nowhere.org'),
  first_name = CONCAT('FIRST_NAME_', id),
  last_name  = CONCAT('LAST_NAME_', id),
  username   = CONCAT('username', id);

UPDATE zambia.partners_partnerorganization
SET
  name          = CONCAT('Partner', id),
  address       = CONCAT('Address', id),
  email         = CONCAT('email', id, '@nowhere.org'),
  phone_number  = id,
  vendor_number = id,
  total_ct_cp   = id,
  total_ct_cy   = id,
  net_ct_cy     = id,
  city          = CONCAT('City ', id);

UPDATE _SCHEMA_.reports_indicator
SET name = CONCAT('Report', id);

UPDATE _SCHEMA_.reports_result
SET name = CONCAT('Result', id);

-- UPDATE _SCHEMA_.funds_fundsreservationitem
-- SET
--   donor             = CONCAT('Donor', id),
--   overall_amount    = id,
--   overall_amount_dc = id;

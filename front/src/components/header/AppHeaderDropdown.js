import React, { useState, useEffect } from 'react'
import {
  CAvatar,
  CBadge,
  CDropdown,
  CDropdownDivider,
  CDropdownItem,
  CDropdownMenu,
  CDropdownToggle,
} from '@coreui/react'
import {
  cilBell,
  cilCreditCard,
  cilSettings,
  cilUser,
  cilExitToApp,
} from '@coreui/icons'
import CIcon from '@coreui/icons-react'
import { getCookies, setCookie } from 'src/helpers/_auth'
import jobParserClient from 'src/client/Client'
import {formatRoute} from "react-router-named-routes/lib";
import {ROUTES} from "src/routes";
import {NavLink} from "react-router-dom";

const AppHeaderDropdown = () => {
  const [avatarInitials, setAvatarInitials] = useState(null);

  useEffect(() => {
    const fetchAvatarInitials = async () => {
      const cookies = getCookies();
      if (!cookies || !cookies.avatarInitials) {
        jobParserClient.client.defaults.headers['Authorization'] = `Bearer ${cookies.accessToken}`;
        const user_data = await jobParserClient.users.getMe();
        const initials = user_data.first_name.charAt(0) + user_data.last_name.charAt(0);
        setCookie('avatarInitials', initials, 1);
        setAvatarInitials(initials);
      } else {
        setAvatarInitials(cookies.avatarInitials);
      }
    };

    fetchAvatarInitials();
  }, []);

  return (
    <CDropdown variant="nav-item">
      <CDropdownToggle placement="bottom-end" className="py-0 pe-0" caret={false}>
        <CAvatar color="primary" textColor="white" size="md">
          {avatarInitials}
        </CAvatar>
      </CDropdownToggle>
      <CDropdownMenu className="pt-0" placement="bottom-end">
        <CDropdownItem to={formatRoute(ROUTES.PROFILE)} as={NavLink}>
          <CIcon icon={cilUser} className="me-2" />
          Profile
        </CDropdownItem>
        <CDropdownItem to={formatRoute(ROUTES.SETTINGS)} as={NavLink}>
          <CIcon icon={cilSettings} className="me-2" />
          Settings
        </CDropdownItem>
        <CDropdownItem to={formatRoute(ROUTES.SUBSCRIPTIONS)} as={NavLink}>
          <CIcon icon={cilCreditCard} className="me-2" />
          Subscription
        </CDropdownItem>
        <CDropdownDivider />
        <CDropdownItem href="#">
          <CIcon icon={cilExitToApp} className="me-2" />
          Logout
        </CDropdownItem>
      </CDropdownMenu>
    </CDropdown>
  );
};

export default AppHeaderDropdown;

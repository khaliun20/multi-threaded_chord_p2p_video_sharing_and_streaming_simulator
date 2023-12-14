import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';

function Dropdown() {
  return (
      <Container>
          <Nav>
            <NavDropdown
              id="nav-dropdown-dark-example"
              title={<span style={{ color: 'white' }}>Videos</span>}
              menuVariant="dark"
            >
              <NavDropdown.Item href="#action/3.1">DNA Transcription</NavDropdown.Item>
              <NavDropdown.Item href="#action/3.2">Big Bucks Bunny</NavDropdown.Item>
            </NavDropdown>
          </Nav>
      </Container>
  );
}

export default Dropdown;
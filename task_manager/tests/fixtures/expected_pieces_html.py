EXPECTED_HTML_FILTERS_ARE_NOT_SET = """<tbody>
        
          <tr>
            <td>1</td>
            <td>
              <a href="/tasks/1/">deploy</a>
            </td>
            <td>active</td>
            <td>ilon mask</td>
            
              <td>ilon mask</td>
            
            <td>15.07.2024 17:00</td>
            <td>
              <a href="/tasks/1/update/"
                >Изменить</a
              >
              <br />
              <a href="/tasks/1/delete/"
                >Удалить</a
              >
            </td>
          </tr>
        
          <tr>
            <td>2</td>
            <td>
              <a href="/tasks/2/">fix</a>
            </td>
            <td>frozen</td>
            <td>taylor swift</td>
            
              <td>ilon mask</td>
            
            <td>15.07.2024 17:00</td>
            <td>
              <a href="/tasks/2/update/"
                >Изменить</a
              >
              <br />
              <a href="/tasks/2/delete/"
                >Удалить</a
              >
            </td>
          </tr>
        
      </tbody>"""

EXPECTED_HTML_FILTERS_ARE_SET = """<tbody>
        
          <tr>
            <td>2</td>
            <td>
              <a href="/tasks/2/">fix</a>
            </td>
            <td>frozen</td>
            <td>taylor swift</td>
            
              <td>ilon mask</td>
            
            <td>15.07.2024 17:00</td>
            <td>
              <a href="/tasks/2/update/"
                >Изменить</a
              >
              <br />
              <a href="/tasks/2/delete/"
                >Удалить</a
              >
            </td>
          </tr>
        
      </tbody>"""

EXPECTED_HTML_FILTERS_ARE_SET_REQUEST_USER_TASKS_ONLY = """<tbody>
        
          <tr>
            <td>1</td>
            <td>
              <a href="/tasks/1/">deploy</a>
            </td>
            <td>active</td>
            <td>ilon mask</td>
            
              <td>ilon mask</td>
            
            <td>15.07.2024 17:00</td>
            <td>
              <a href="/tasks/1/update/"
                >Изменить</a
              >
              <br />
              <a href="/tasks/1/delete/"
                >Удалить</a
              >
            </td>
          </tr>
        
      </tbody>"""

EXPECTED_HTML_FILTERS_ARE_SET_EMPTY_QUERYSET = """<tbody>
        
      </tbody>"""

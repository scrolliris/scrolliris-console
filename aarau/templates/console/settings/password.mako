<%namespace file='aarau:templates/macro/_error_message.mako' import="render_error_message"/>
<%namespace file='aarau:templates/macro/_flash_message.mako' import="render_notice"/>
<%namespace file='aarau:templates/macro/_title.mako' import="render_title"/>

<%inherit file='aarau:templates/console/_layout.mako'/>

<%block name='title'>${render_title('Password - Settings')}</%block>

<%block name='sidebar'>
  <%include file='aarau:templates/console/_sidebar.mako'/>
</%block>

<div class="content">
  <div id="settings">
    <div class="grid">
      <div class="row">
        <div class="column-16">
          ${render_notice()}
        </div>
      </div>

      <div class="row">
        <div class="column-16">
          <div class="attached header"><h5>Password</h5></div>
          <div class="attached box">
            <form id="change_password" class="form${' error' if err_msg else ' success' if suc_msg else ''}" action="${req.route_url('console.settings.section', section='password', subdomain='')}" method="post">
              ${form.csrf_token}
              <div class="row">
                <div class="required field-8 field-v-12 field-l-16${' error' if form.current_password.errors else ''}">
                  <label class="label" for="current_password">Current password</label>
                  ${form.current_password(class_='', autocomplete='current-password')}
                  ${render_error_message(form.current_password)}
                </div>
              </div>
              <div class="row">
                <div class="required field-8 field-v-12 field-l-16${' error' if form.new_password.errors else ''}">
                  <label class="label" for="new_password">New password</label>
                  ${form.new_password(class_='', autocomplete='new-password')}
                  ${render_error_message(form.new_password)}
                </div>
              </div>
              <div class="row">
                <div class="required field-8 field-v-12 field-l-16${' error' if form.new_password_confirmation.errors else ''}">
                  <label class="label" for="new_password_confirmation">New password confirmation</label>
                  ${form.new_password_confirmation(class_='', autocomplete='off')}
                  ${render_error_message(form.new_password_confirmation)}
                </div>
              </div>
              ${form.submit(class_='primary flat button')}
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

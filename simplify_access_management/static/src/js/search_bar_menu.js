/** @odoo-module **/
import { SearchBarMenu } from "@web/search/search_bar_menu/search_bar_menu";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { onWillStart, useState } from "@odoo/owl";

patch(SearchBarMenu.prototype, {
  setup() {
    super.setup(...arguments);
    this.orm = useService("orm");
    onWillStart(async () => {
      const res = await this.orm.call("access.management", "get_hidden_field", [
        "",
        this?.env?.searchModel?.resModel,
      ]);
      this.fields = this.fields.filter((ele) => !res.includes(ele.name));
    });
  },
});

odoo.define('rail_automatic_pricelist.ProductScreen', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const NumberBuffer = require('point_of_sale.NumberBuffer');
    const { Gui } = require('point_of_sale.Gui');
    const { useListener } = require("@web/core/utils/hooks");
    const Registries = require('point_of_sale.Registries');
    const { onMounted, onWillUnmount, useRef, useState } = owl;

    const PromotionProductScreenRail = (ProductScreen) =>
        class extends ProductScreen {

            async _updateSelectedOrderline(event) {
                var updated_line =  super._updateSelectedOrderline(...arguments);
                this.currentOrder.apply_pricelist();
                return updated_line
            }

      }
    Registries.Component.extend(ProductScreen, PromotionProductScreenRail);

    return ProductScreen;

});

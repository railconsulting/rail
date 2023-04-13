  odoo.define('rail_automatic_pricelist.models', function (require) {
"use strict";

    const {PosGlobalState, Order, Orderline} = require('point_of_sale.models');
    const Registries = require('point_of_sale.Registries');
    const OrderSummary = require('point_of_sale.OrderSummary');
    const core = require('web.core');
    var QWeb = core.qweb;
    var { Gui } = require('point_of_sale.Gui');
    var _t = core._t;

    const OrderPricelist = (Order) =>
        class OrderPricelist extends Order {

            constructor(obj, options) {
                super(...arguments);
                this.total_qty = this.total_qty || 0;
            }

            export_as_JSON() {
                const json = super.export_as_JSON(...arguments);
                json.total_qty = this.total_qty
                json.pricelist_id = this.pricelist.id
                return json;
            }
            //@override
            init_from_JSON(json) {
                super.init_from_JSON(...arguments);
                this.total_qty = json.total_qty;
            }
            //@override
            export_for_printing() {
                const json = super.export_for_printing(...arguments);
                json.total_qty = this.total_qty;
                return json;
            }

            add_product(product, options){
                super.add_product(...arguments);
                this.apply_pricelist();
            }

            apply_pricelist(){
                var totalQty = this.orderlines.map(orderline => orderline.quantity).reduce((a, b) => a + b, 0);
                this.total_qty = totalQty;
                var newPricelist = this.pos.pricelists.filter(pricelist => totalQty >= pricelist.min_quantity && totalQty <= pricelist.max_quantity)
                || this.pos.default_pricelist;
                if (newPricelist.length > 0){
                    var sequences = newPricelist.map(pricelist => pricelist.sequence);
                    var get_sequence = Math.min.apply(Math, sequences)
                    var pricelist_to_be_updated = newPricelist.filter(pl => pl.sequence == get_sequence)
                    this.set_pricelist(pricelist_to_be_updated[0]);
                }
            }

        }

    Registries.Model.extend(Order, OrderPricelist);

    const OrderlinePricelist = (Orderline) =>
        class extends Orderline {

        set_quantity(quantity, keep_price){
            var settled = super.set_quantity(...arguments);
            this.order.apply_pricelist();
            return settled
        }

    }
    Registries.Model.extend(Orderline, OrderlinePricelist);

});